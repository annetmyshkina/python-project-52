from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Labels


class LabelForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter label name"),
                }
            )
        }
        labels = {"name": _("Name")}
        error_messages = {
            "name": {
                "unique": _("already exists"),
            }
        }
