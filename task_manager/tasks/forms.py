from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses

from .models import Tasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ["name", "description", "status", "executor", "labels"]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor": _("Executor"),
            "labels": _("Labels"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "executor": forms.Select(attrs={"class": "form-select"}),
            "labels": forms.SelectMultiple(
                attrs={
                    "class": "form-select",
                    "size": 8,
                    "style": "height: 200px;",
                }
            ),
        }
        error_messages = {
            "name": {"unique": _("already exists")},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].queryset = Statuses.objects.all()
        self.fields["status"].empty_label = _("----")

        self.fields["executor"].queryset = User.objects.all()
        self.fields["executor"].empty_label = _("----")
        self.fields["executor"].label_from_instance = lambda obj: (
            obj.get_full_name() or obj.username
        )

        self.fields["labels"].queryset = Labels.objects.all()
