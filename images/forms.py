from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _

from images.models import Dataset, Experiment, PRIMITIVES_CHOICES
from users.models import Team


class FormDataset(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label=_("Name"))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("1024 characters maximum"),
                                                               "rows": 3}),
                                  label=_("Description"))

    class Meta:
        model = Dataset
        fields = ('name', 'description')


class NewModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class FormTag(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Name")}), label=False, required=True)
    type = forms.ChoiceField(choices=PRIMITIVES_CHOICES, label=False, required=True)
    color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}), required=True, label=False)


TagFormset = formset_factory(FormTag, extra=1)


class FormExperiment(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(), label=_("Name"))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("1024 characters maximum"),
                                                               "rows": 3}),
                                  label=_("Description"))
    dataset = NewModelChoiceField(queryset=Dataset.objects.all(), label=_("Dataset"))
    team = NewModelChoiceField(queryset=Team.objects.all(), label=_("Team"))

    class Meta:
        model = Experiment
        fields = ('name', 'description', 'dataset', 'team')
