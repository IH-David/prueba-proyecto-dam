# Importa la clase UserCreationForm desde Django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# Define tu clase de formulario personalizado que hereda de UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control password-input',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required':'required',
        }
    ))
    
    password2 = forms.CharField(label = 'Contraseña de confirmacion', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control password-input',
            'placeholder': 'Ingrese otra vez su contraseña...',
            'id': 'password2',
            'required':'required',
        }
    ))
    
    username = forms.CharField(label = 'Nombre de usuario', widget = forms.TextInput(
        attrs = {
            'class': 'form-control username-input',
            'placeholder': 'Ingrese su nombre...',
            'id': 'username',
            'required':'required',
        }
    ))
    
