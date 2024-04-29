from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Libro

# formularios usuarios
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    birth_date = forms.DateField(required=False, help_text='Optional. Format: YYYY-MM-DD')
    phone_number = forms.CharField(max_length=15, required=False, help_text='Optional.')
    address = forms.CharField(max_length=100, required=False, help_text='Optional.')
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'phone_number', 'address')
    # Sobreescribir el metodo de guardado de user 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Establecer al usuario como no miembro del personal (staff)
        user.is_superuser = False  # Establecer al usuario como no superusuario
        if commit:
            user.save()
        return user

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'birth_date', 'phone_number', 'address']

        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomUserModificacionForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'phone_number', 'address', 'password']

    password = forms.CharField(widget=forms.PasswordInput, required=False)




# formularios libros
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'categoria', 'precio', 'descripcion', 'src_imagen']


class LibroModificacionForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['categoria', 'titulo', 'descripcion', 'precio', 'src_imagen']





