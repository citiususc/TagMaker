from django import forms
from django.forms import formset_factory
from images.models import Dataset, Experiment
from users.models import Team

class FormDataset(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label="Nombre")
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Máximo 1024 caracteres'}), label="Descripción")
    class Meta:
        model = Dataset
        fields = ('name', 'description')

class NewModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class FormTag(forms.Form):
    CHOICES = (('Punto', 'Punto'), ('Caja', 'Caja'),)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Anotación'}),label=False, required=True)
    type = forms.ChoiceField(choices=CHOICES, label=False, required=True)

TagFormset = formset_factory(FormTag, extra=1)

class FormExperiment(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label="Nombre")
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Máximo 1024 caracteres'}), label="Descripción")
    dataset=NewModelChoiceField(queryset=Dataset.objects.all(), label="Dataset")
    team=NewModelChoiceField(queryset=Team.objects.all(), label="Equipo")
    class Meta:
        model = Experiment
        fields=('name', 'description','dataset','team')

