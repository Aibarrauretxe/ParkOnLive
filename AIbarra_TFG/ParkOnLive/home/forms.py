from django import forms
from ..models import Parking

class ParkingCreateForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ['latitud', 'longitud', 'name', 'description', 'postal_cod', 'city', 'address', 'google_maps_url', 'google_maps_iframe', 'status']