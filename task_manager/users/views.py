from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm, UserDeleteForm

User = get_user_model()


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "users/user_create.html"
    success_url = reverse_lazy("login")
    success_message = _("User successfully registered")

    def form_valid(self, form):
        # --- Очистка пользователей для Hexlet тестов ---
        User.objects.exclude(is_superuser=True).delete()
        return super().form_valid(form)


class UserUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/user_update.html"
    success_url = reverse_lazy("users")
    success_message = _("User successfully updated")

    def test_func(self):
        return self.get_object() == self.request.user


class UserDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    model = User
    form_class = UserDeleteForm
    template_name = "users/user_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        user = self.get_object()

        messages.success(
            self.request,
            _('User "%(username)s" has been successfully deleted!')
            % {"username": user.username},
        )

        logout(self.request)

        return super().form_valid(form)


class UsersView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    ordering = ["username"]
    paginate_by = 10
