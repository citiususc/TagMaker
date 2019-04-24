from django import forms
from imagenes.models import Dataset, Experimento
from usuarios.models import Equipo

class FormDataset(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Descripción. Máximo 1024 caracteres'}))
    class Meta:
        model = Dataset
        fields = ('name', 'description')


class NewModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name


class FormExperimento(forms.ModelForm):
    dataset=NewModelChoiceField(queryset=Dataset.objects.all())
    equipo=NewModelChoiceField(queryset=Equipo.objects.all())
    class Meta:
        model=Experimento
        fields=('name', 'description','dataset','equipo')

