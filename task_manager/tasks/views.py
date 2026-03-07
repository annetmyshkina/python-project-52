import django_filters
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses

from .forms import TaskForm
from .models import Tasks


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tasks
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully created")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        task.save()

        if form.cleaned_data["labels"]:
            task.labels.set(form.cleaned_data["labels"])

        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully updated")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()

        if form.cleaned_data["labels"]:
            task.labels.set(form.cleaned_data["labels"])

        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.author != self.request.user:
            messages.error(self.request, _("Only the task creator can delete a task"))
            return redirect("tasks")
        return obj

    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            _('Task deleted successfully')
        )
        return super().delete(request, *args, **kwargs)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Tasks
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        label=_("Status"),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label=_("Executor")
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(), method="filter_label", label=_("Label")
    )
    my_tasks = django_filters.BooleanFilter(
        method="filter_my_tasks",
        label=_("My tasks"),
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Tasks
        fields = []

    def filter_label(self, queryset, _, value):
        return queryset.filter(labels=value) if value else queryset

    def filter_my_tasks(self, queryset, _, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset


class TasksView(LoginRequiredMixin, FilterView):
    model = Tasks
    template_name = "tasks/tasks_list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    ordering = ["name"]
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("status", "author", "executor")
            .prefetch_related("labels")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
