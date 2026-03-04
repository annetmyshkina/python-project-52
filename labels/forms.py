from django import forms
from .models import Labels
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter label name')
            })
        }
        labels = {'name': _('Name')}
        error_messages = {
            'name': {
                'unique': _('Label with this name already exists'),
                'required': _('Name cannot be empty')
            }
        }