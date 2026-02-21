
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.list import ListView

class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(AuthLoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy('home')

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class UsersView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'
    paginate_by = 10