from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_("Name"), max_length=30, required=True, help_text=_('Mandatory'))
    last_name = forms.CharField(label=_("Surname"), max_length=30, required=True, help_text=_('Mandatory'))
    email = forms.EmailField(label=("Email"), max_length=254, required=True,
                             help_text=_('Mandatory. Be sure to introduce a valid address'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class EditProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
