from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError

from .forms import UserRegistrationForm, ProviderRegistrationForm
from ..models import Provider


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        login_failed = False

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            if not remember_me:
                # Si remember_me no está marcado, usa la configuración predeterminada de la duración de la sesión
                pass
            else:
                # Si remember_me está marcado, configura la duración de la sesión para ser más larga
                request.session.set_expiry(3600 * 24 * 30)  # Por ejemplo, 30 días en segundos
            return redirect('home_view')  # Redirect to dashboard or any other page after login
        else:
            # Si la autenticación falla, muestra un mensaje de error
            messages.error(request, '<b>Credenciales inválidas.</b><br>Por favor, inténtelo de nuevo.')
            
            # Cambiamos el estado a login fallido.
            login_failed = True

    # Si llegamos aquí, es porque hubo un error en el inicio de sesión
    return render(request, 'home.html', {'login_form': UserRegistrationForm, 'username': username, 'login_failed': login_failed})

def logout(request):
    django_logout(request)
    return redirect('home_view')  # Redirige a la página de inicio u otra página después de cerrar sesión

def user_signup(request):
    errors = []
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home_view')  # Redirect to success page
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    error_message = form.fields[field].error_messages.get(error, error)
                    if "Passwords don't match." in error_message:
                        error_message = "Las contraseñas no coinciden."
                    errors.append(f"{error_message}")

    else:
        form = UserRegistrationForm()
        
    # If request method is POST and form is not valid, form.errors will contain errors.
    # We pass these errors to the template.
    
    return render(request, 'user_signup.html', {'form': form, 'errors': errors})

def provider_signup(request):
    errors = []

    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            # Asigna el usuario actual al campo 'user' del modelo antes de guardar el formulario
            provider = form.save(commit=False)
            provider.user = request.user
            provider.save()
            return redirect('home_view')  # Redirige a la página de inicio
        else:
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    error_message = form.fields[field].error_messages.get(error, error)
                    errors.append(f"{error_message}")
    else:
        form = ProviderRegistrationForm()

    return render(request, 'provider_signup.html', {'form': form, 'errors': errors})

@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')  # Nuevo campo para el proveedor
        nif = request.POST.get('nif')  # Nuevo campo para el proveedor

        try:
            # Actualiza el usuario con los nuevos datos
            request.user.username = username
            request.user.email = email
            request.user.save()

            # Intenta obtener el proveedor asociado al usuario
            provider = Provider.objects.filter(user=request.user).first()
            if provider:
                # Si existe el proveedor, actualiza sus datos
                provider.name = name
                provider.nif = nif
                provider.save()

            return JsonResponse({'message': '¡Cambios guardados exitosamente!'})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            print(f'Error al guardar los cambios del usuario: {str(e)}')
            return JsonResponse({'error': f'Hubo un error al guardar los cambios: {str(e)}'}, status=500)
    else:
        # Buscar proveedor por nombre de usuario
        is_provider = False
        try:
            provider = Provider.objects.get(user__username=request.user.username)
            profile_data = {
                'username': provider.user.username,
                'email': provider.user.email,
                'name': provider.name,
                'nif': provider.nif,
                # Otros datos del perfil del proveedor...
            }
            is_provider = True
        except Provider.DoesNotExist:
            # Si el usuario no es proveedor, usa sus datos de usuario
            profile_data = {
                'username': request.user.username,
                'email': request.user.email,
                # Otros datos del perfil del usuario...
            }
        
        return render(request, 'profile.html', {'profile_data': profile_data, 'is_provider': is_provider})