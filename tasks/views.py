from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth.models import User
from statuses.models import Statuses
from .models import Tasks
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from .forms import TaskForm


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("tasks")
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("tasks")
    success_message = _('Task successfully updated')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, _('You cannot delete this task.'))
            raise Http404(_("You cannot delete this task."))
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(
            request,
            _('Task "%(name)s" deleted successfully') % {'name': obj.name}
        )
        return super().delete(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

class TasksView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"
    ordering = ["name"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status")
        executor = self.request.GET.get("executor")

        if status:
            queryset = queryset.filter(status__pk=status)
        if executor:
            queryset = queryset.filter(executor__pk=executor)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Statuses.objects.all()
        context["executors"] = User.objects.all()
        context["selected_status"] = self.request.GET.get("status")
        context["selected_executor"] = self.request.GET.get("executor")
        return context


