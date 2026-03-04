from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import LabelForm
from .models import Labels


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Labels
    form_class = LabelForm
    template_name = "labels/label_create.html"
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully created")


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = "labels/label_update.html"
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully updated")


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Labels
    template_name = "labels/label_delete.html"
    success_url = reverse_lazy("labels")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            count = self.object.tasks.count()
            messages.warning(
                request,
                _('Label "%(name)s" used in %(count)d tasks')
                % {"name": self.object.name, "count": count},
            )
            return redirect("labels")

        messages.success(
            request,
            _('Label "%(name)s" deleted successfully')
            % {"name": self.object.name},
        )
        return self.delete(request, *args, **kwargs)


class LabelsView(LoginRequiredMixin, ListView):
    model = Labels
    template_name = "labels/labels_list.html"
    context_object_name = "labels"
    ordering = ["name"]
    paginate_by = 10
