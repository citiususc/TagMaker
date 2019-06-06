from django import forms
from django.forms import formset_factory
from images.models import Dataset, Experiment
from users.models import Team

class FormDataset(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Descripción. Máximo 1024 caracteres'}))
    class Meta:
        model = Dataset
        fields = ('name', 'description')


class NewModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

class FormTag(forms.Form):
    CHOICES = (('Punto', 'Punto'), ('Caja', 'Caja'),)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Anotación'}))
    type = forms.ChoiceField(choices=CHOICES)

TagFormset = formset_factory(FormTag, extra=1)

class FormExperiment(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Descripción. Máximo 1024 caracteres'}))
    dataset=NewModelChoiceField(queryset=Dataset.objects.all())
    team=NewModelChoiceField(queryset=Team.objects.all())
    class Meta:
        model = Experiment
        fields=('name', 'description','dataset','team')

