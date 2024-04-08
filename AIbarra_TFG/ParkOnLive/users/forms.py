from django import forms
from django.contrib.auth.models import User
from ..models import Provider

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        error_messages = {
            'username': {
                'required': 'El nombre de usuario es requerido.',
                'unique': 'Este nombre de usuario ya está en uso.'
            },
            'email': {
                'required': 'El correo electrónico es requerido.',
                'unique': 'Este correo electrónico ya está en uso.',
                'invalid': 'Por favor, introduce una dirección de correo electrónico válida.'
            },
            'password': {
                'required': 'La contraseña es requerida.'
            },
            'password_confirm': {
                'required': 'Por favor, confirma tu contraseña.',
                'password_mismatch': 'Las contraseñas no coinciden.'
            }
        }

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise forms.ValidationError("Passwords don't match.")
        return cleaned_data['password_confirm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    

class ProviderRegistrationForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['nif', 'name', 'token']
        widgets = {
            'nif': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }