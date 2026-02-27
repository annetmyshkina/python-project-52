
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import CustomUserChangeForm, CustomUserCreationForm, UserDeleteForm


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "User successfully registered!")
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users")

    def test_func(self):
        return self.get_object() == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    form_class = UserDeleteForm
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object() == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "The user has been successfully deleted!")
        logout(self.request)
        return super().form_valid(form)


class UsersView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    ordering = ["username"]
    paginate_by = 10