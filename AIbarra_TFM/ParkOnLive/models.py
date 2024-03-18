from django.db import models
from .users.models import CustomUser
    
class Parking(models.Model):
    provider = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    google_maps_url = models.URLField()
    status = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

class FavouriteParkings(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, null=True, on_delete=models.CASCADE)

class ParkingOcupation(models.Model):
    parking = models.ForeignKey(Parking, null=True, on_delete=models.CASCADE)
    current_ocupation = models.IntegerField()
    maximum_ocupation = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
