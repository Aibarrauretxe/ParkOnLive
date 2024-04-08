import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIbarra_TFG.settings')

import random
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone

from ..ParkOnLive.models import Provider, Parking, FavouriteParkings, ParkingOccupancy
from django.db.utils import IntegrityError

fake = Faker()

def create_users(num_users):
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(username=username, email=email, password=password)
        users.append(user)
    return users

def create_providers(num_providers, users):
    providers = []
    for _ in range(num_providers):
        user = random.choice(users)
        nif = fake.random_int(min=10000000, max=99999999)
        name = fake.company()
        provider = Provider.objects.create(user=user, nif=nif, name=name)
        providers.append(provider)
    return providers

def create_parkings(num_parkings, providers):
    parkings = []
    for _ in range(num_parkings):
        provider = random.choice(providers)
        latitud = fake.latitude()
        longitud = fake.longitude()
        name = fake.street_name()
        description = fake.text()
        postal_cod = fake.postcode()
        city = fake.city()
        address = fake.address()
        google_maps_url = fake.url()
        status = random.choice(['Activo', 'Inactivo'])
        parking = Parking.objects.create(provider=provider, latitud=latitud, longitud=longitud,
                                         name=name, description=description, postal_cod=postal_cod,
                                         city=city, address=address, google_maps_url=google_maps_url,
                                         status=status)
        parkings.append(parking)
    return parkings

def create_favourite_parkings(num_favourites, users, parkings):
    favourite_parkings = []
    for _ in range(num_favourites):
        user = random.choice(users)
        parking = random.choice(parkings)
        try:
            favourite = FavouriteParkings.objects.create(user=user, parking=parking)
            favourite_parkings.append(favourite)
        except IntegrityError:
            pass  # Ignore IntegrityError if a duplicate favourite is created
    return favourite_parkings

def create_parking_occupancies(num_occupancies, parkings):
    occupancies = []
    for _ in range(num_occupancies):
        parking = random.choice(parkings)
        occupancy_current = random.randint(0, 100)
        occupancy_max = random.randint(100, 200)
        timestamp = fake.date_time_between(start_date="-1y", end_date="now")
        occupancy = ParkingOccupancy.objects.create(parking=parking, occupancy_current=occupancy_current,
                                                    occupancy_max=occupancy_max, timestamp=timestamp)
        occupancies.append(occupancy)
    return occupancies

def generate_data():
    # Crear usuarios
    num_users = 10
    users = create_users(num_users)

    # Crear proveedores
    num_providers = 5
    providers = create_providers(num_providers, users)
    for provider in providers:
        print(provider)

    # Crear parkings
    num_parkings = 20
    parkings = create_parkings(num_parkings, providers)
    for parking in parkings:
        print(parking)

    # Crear parkings favoritos
    num_favourites = 30
    favourite_parkings = create_favourite_parkings(num_favourites, users, parkings)
    for favourite_parking in favourite_parkings:
        print(favourite_parking)

    # Crear ocupaciones de parking
    num_occupancies = 50
    occupancies = create_parking_occupancies(num_occupancies, parkings)
    for occupancie in occupancies:
        print(occupancie)

    print("Datos generados exitosamente!")

if __name__ == "__main__":
    generate_data()
