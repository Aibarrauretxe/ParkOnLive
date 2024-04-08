from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nif = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    register_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new instance
            self.modified_date = timezone.now()  # Set modified_date only on creation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Parking(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    serial = models.AutoField(primary_key=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    register_date = models.DateTimeField(default=timezone.now)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    postal_cod = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    google_maps_url = models.URLField()
    google_maps_iframe = models.CharField(max_length=512)
    status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        # Actualizar la fecha de modificación al guardar
        self.modification_date = timezone.now()
        super(Parking, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class FavouriteParkings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parking = models.ForeignKey('Parking', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite parking: {self.parking.name}"
    
class ParkingOccupancy(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    occupancy_current = models.IntegerField()
    occupancy_max = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.parking.name} - {self.occupancy_current}/{self.occupancy_max} ({self.timestamp})"