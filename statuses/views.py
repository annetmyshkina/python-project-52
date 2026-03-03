from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Statuses
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from .forms import StatusForm


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Statuses
    form_class = StatusForm
    template_name = "statuses/status_create.html"
    success_url = reverse_lazy("statuses")
    success_message = _('Status successfully created')


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = "statuses/status_update.html"
    success_url = reverse_lazy("statuses")
    success_message = _('Status successfully updated')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Statuses
    template_name = "statuses/status_delete.html"
    success_url = reverse_lazy("statuses")

    def post(self, request, *args, **kwargs):
        if self.object.tasks.exists():
            count = self.object.tasks.count()
            messages.error(
                request,
                _('Cannot delete status "%(name)s". It is used in %(count)d tasks.') % {
                    'name': self.object.name,
                    'count': count
                }
            )
            return redirect('statuses')

        messages.success(
            request,
            _('Status "%(name)s" deleted successfully') % {'name': self.object.name}
        )
        return self.delete(request, *args, **kwargs)


class StatusesView(LoginRequiredMixin, ListView):
    model = Statuses
    template_name = "statuses/statuses_list.html"
    context_object_name = "statuses"
    ordering = ["name"]
    paginate_by = 10
