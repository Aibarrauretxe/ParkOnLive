from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json


from ..models import Provider, Parking, FavouriteParkings, ParkingOccupancy

from .forms import ParkingCreateForm

def home(request):
    # Aquí obtienes el usuario actualmente autenticado
    user = request.user
    
    is_provider = False
    
    try:
        # Intenta obtener el provider asociado al usuario
        provider = Provider.objects.filter(user=request.user).first()
        if provider:
            is_provider = True
    except TypeError:
        pass
    return render(request, 'home.html', {'user': user, 'is_provider': is_provider})

def parking_create(request):
    errors = []
    
    provider = Provider.objects.filter(user=request.user).first()
    is_provider = provider != None
    if request.method == 'POST':
        form = ParkingCreateForm(request.POST)
        if form.is_valid():
            parking = form.save(commit=False)
            parking.provider = provider  # Asigna el usuario actual como el provider del parking
            parking.save()

            return redirect('home_view')  # Redirect to success page
        
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    error_message = form.fields[field].error_messages.get(error, error)
                    errors.append(f"{error_message}")
    else:
        form = ParkingCreateForm()
        
        return render(request, 'parking_create.html', {'form': form, 'provider': provider, 'errors': errors, 'is_provider': is_provider})
    return render(request, 'parking_create.html', {'form': form, 'errors': errors})

def parkings_provider(request):
    provider = Provider.objects.filter(user=request.user).first()
    
    parkings = None
    if provider:
        # Obtener todos los parkings asociados al provider actual (puedes ajustar esta lógica según tu implementación)
        parkings = Parking.objects.filter(provider=provider)

    # Pasar los parkings al template para ser mostrados
    return render(request, 'parkings_provider.html', {'parkings': parkings, 'is_provider': True})

def edit_parking(request, pk):
    errors = []
    
    provider = Provider.objects.filter(user=request.user).first()
    
    # Obtener el parking que se desea editar
    parking = get_object_or_404(Parking, pk=pk)

    if request.method == 'POST':
        # Si se envió el formulario, procesar los datos recibidos
        form = ParkingCreateForm(request.POST, instance=parking)
        if form.is_valid():
            form.save()
            return redirect('parkings_provider_view')  # Reemplaza 'parkings_provider_view' con el nombre de la vista donde se muestra la lista de parkings
        
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    error_message = form.fields[field].error_messages.get(error, error)
                    errors.append(f"{error_message}")
    else:
        # Si es una solicitud GET, mostrar el formulario para editar el parking
        form = ParkingCreateForm(instance=parking)

    return render(request, 'edit_parking.html', {'form': form, 'errors': errors, 'parking': parking, 'provider': provider})  # Reemplaza 'editar_parking.html' con el nombre del template generado

def delete_parking(request, pk):
    # Obtener el parking que se desea borrar
    parking = get_object_or_404(Parking, pk=pk)

    if request.method == 'POST':
        # Si se confirmó la eliminación, borrar el parking y redirigir a la lista de parkings
        parking.delete()
        return redirect('parkings_provider_view')  # Reemplaza 'parkings_provider' con el nombre de la vista donde se muestra la lista de parkings

    return render(request, 'parkings_provider.html', {'parking': parking})

def parkings(request):
    # Obtención de parametros de filtrado recibidos desde la vista HTML.
    # Filtro Status del Parking
    status = request.GET.get('status', None)
    
    # Filtro Ciudad del Parking
    city = request.GET.get('city', None)
    
    # Filtro Codigo Postal del Parking
    postal_cod = request.GET.get('postal_cod', None)
    
    # Filtro Favoritos del Parking
    favourites = request.GET.get('favourites', None)
    
    # Valores que deberan de ser verificados para filtrar
    filter_vals = {}
    vals = {
        'status': status,
        'city': city,
        'postal_cod': postal_cod
    }
    
    # Solamente se filtraran aquellos que tengan algun valor.
    for key, val in vals.items():
        if val and val != '':
            filter_vals[f"{key}__icontains"] = val
    
    # Si se solicita algun filtro se utilizara la función de filtrado para objetos Django.
    if len(filter_vals.keys()) > 0:
        parkings = Parking.objects.filter(**filter_vals)
    else:
        # En caso de no solicitarse ningun filtro se obtendran todos los parkings.
        parkings = Parking.objects.all()
    
    # Una vez tenemos los parkings filtrados o no procederemos a verificar si se requieren solo los favoritos.
    # Para ello obtenemos el usuario logeado.
    user = request.user  
    # Verificamos si hay usuario y se requiere de filtrar por favoritos
    if user.is_authenticated and favourites == 'on':
        # Si el usuario está autenticado
        favourite_parkings = []
        for parking in parkings:
            # Intenta obtener el objeto FavouriteParkings para el usuario y el parking actual
            favorite_parking = FavouriteParkings.objects.filter(user=user, parking=parking).first()
            
            # Si se encontró el objeto FavouriteParkings, el parking es favorito para el usuario
            if favorite_parking:
                parking.is_favorite = True
                favourite_parkings.append(parking)
            else:
                parking.is_favorite = False
       
        parkings = favourite_parkings
                
    # Obtenemos las ocupaciones de los parkings listados.
    for parking in parkings:
        # Intenta obtener el objeto FavouriteParkings para el usuario y el parking actual
        parking_occupancy_register = ParkingOccupancy.objects.filter(parking=parking).last()
        
        # Si tenemos ocupación del parking disponible generaremos las variables calculadas.
        if parking_occupancy_register:
            parking.occupancy_current = parking_occupancy_register.occupancy_current
            parking.occupancy_maximum = parking_occupancy_register.occupancy_max
            
            parking.occupation_percentage = parking.occupancy_current / parking.occupancy_maximum
            parking.occupation_difference = parking.occupancy_maximum - parking.occupancy_current

    # Renderizaremos la vista del listado del parking con las variables requeridas para su funcionamiento.
    return render(request, 'parkings.html', {'parkings': parkings, 'status': status, 'city': city, 'postal_cod': postal_cod, 'favourites': favourites})


@login_required
def toggle_favorite(request, pk):
    # Obtener el parking específico
    parking = get_object_or_404(Parking, pk=pk)
    
    # Verificar si el usuario ya tiene el parking en favoritos
    try:
        favorite_parking = FavouriteParkings.objects.get(user=request.user, parking=parking)
        # Si ya es favorito, lo eliminamos de los favoritos
        favorite_parking.delete()
        message = "Parking eliminado de favoritos."
    except FavouriteParkings.DoesNotExist:
        # Si no es favorito, lo agregamos a los favoritos
        favorite_parking = FavouriteParkings(user=request.user, parking=parking)
        favorite_parking.save()
        message = "Parking añadido a favoritos."
    
    # Puedes redirigir a una página de éxito o simplemente devolver un mensaje
    return HttpResponse(message)

@csrf_exempt
def register_occupancy(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            parking_id = data.get('parking_id')
            occupancy_current = data.get('occupancy_current')
            occupancy_max = data.get('occupancy_max')

            # Verificar si el parking existe
            parking = Parking.objects.get(pk=parking_id)

            # Crear el registro de ocupación
            occupancy = ParkingOccupancy.objects.create(
                parking=parking,
                occupancy_current=occupancy_current,
                occupancy_max=occupancy_max,
                timestamp=timezone.now()
            )

            # Retorna una respuesta JSON con el ID del registro creado
            return JsonResponse({'id': occupancy.id}, status=201)
        except Parking.DoesNotExist:
            return JsonResponse({'error': 'El parking no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)