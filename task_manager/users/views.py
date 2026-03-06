from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
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
        user = self.get_object()
        return self.request.user == user

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        user = self.get_object()
        if request.user != user and not request.user.is_superuser:
            raise PermissionDenied(_("You don't have the rights to change it."))

        return response


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
        messages.success(self.request, _("User has been successfully deleted"))

        logout(self.request)
        return super().form_valid(form)


class UsersView(ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    ordering = ["username"]
    paginate_by = 10
