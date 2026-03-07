from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import StatusForm
from .models import Statuses


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = "statuses/status_create.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Status successfully created")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses")
    success_message = _("Status successfully updated")


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Statuses
    template_name = "statuses/status_delete.html"
    success_url = reverse_lazy("statuses")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tasks.exists():
            messages.warning(
                request,
                _('The status cannot be deleted')
            )
            return redirect("statuses")

        messages.success(
            request, _('Status deleted successfully'))
        return self.delete(request, *args, **kwargs)


class StatusesView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"
    ordering = ["name"]
    paginate_by = 10
