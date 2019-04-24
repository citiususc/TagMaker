from django import forms
from anotaciones.models import Anotacion

class FormAnotacion(forms.ModelForm):
    CHOICES = (('Punto', 'Punto'), ('Caja', 'Caja'),)
    tipo = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = Anotacion
        fields=('anotaciones', 'tipo')