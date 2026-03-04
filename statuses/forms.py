from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Statuses


class StatusForm(forms.ModelForm):
    class Meta:
        model = Statuses
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter status name"),
                }
            )
        }
        labels = {"name": _("Name")}
        error_messages = {
            "name": {
                "unique": _("Status with this name already exists"),
                "required": _("Name cannot be empty"),
            }
        }
