from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField()
    email = models.EmailField()
    
class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    nif = models.CharField(max_length=10)
    created_at  = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=124)
    
class Parking(models.Model):
    parking_id = models.AutoField(primary_key=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.RESTRICT)
    name = models.CharField(max_length=30)
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    created_at  = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    construction_date = models.DateField()
    description = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    google_maps_url = models.URLField()
    status = models.CharField(max_length=1)
    
class FavouriteParking(models.Model):
    parking_id = models.ForeignKey(Parking, on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, on_delete=models.RESTRICT)
    
class Ocupation(models.Model):
    ocupation_id = models.AutoField(primary_key=True)
    parking_id = models.ForeignKey(Parking, on_delete=models.RESTRICT)
    current = models.IntegerField()
    maximum = models.IntegerField()
    timestamp = models.DateTimeField()