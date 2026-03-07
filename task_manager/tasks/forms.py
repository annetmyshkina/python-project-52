from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses

from .models import Tasks


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check"}),
        required=False,
        label=_("Labels"),
    )

    class Meta:
        model = Tasks
        fields = ["name", "description", "status", "executor"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Enter task name"),
                },
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "executor": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "name": {
                "unique": _("already exists"),
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].queryset = Statuses.objects.all()
        self.fields["status"].empty_label = _("----")
        self.fields["executor"].queryset = User.objects.all()
        self.fields["executor"].empty_label = _("----")
