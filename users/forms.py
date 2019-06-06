from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=("Nombre"), max_length=30, required=True, help_text='Obligatorio.')
    last_name = forms.CharField(label=("Apellido"), max_length=30, required=True, help_text='Obligatorio')
    email = forms.EmailField(label=("Email"), max_length=254, required=True, help_text='Obligatorio. Asegúrese de introducir una dirección válida')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields=('username','email','first_name', 'last_name')

