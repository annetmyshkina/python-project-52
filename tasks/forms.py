from django import forms
from statuses.models import Statuses
from .models import Tasks
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter task name')
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'executor': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Statuses.objects.all()
        self.fields['status'].empty_label = _("--------")

        self.fields['executor'].empty_label = _("--------")

