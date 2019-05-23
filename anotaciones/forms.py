from django import forms


class FormAnotacion(forms.Form):
    CHOICES = (('Punto', 'Punto'), ('Caja', 'Caja'),)
    nombre = forms.CharField(max_length=30, required=True)
    tipo = forms.ChoiceField(choices=CHOICES, required=True)
    class Meta:
        fields=('nombre', 'tipo')