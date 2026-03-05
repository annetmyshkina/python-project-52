from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        messages.success(self.request, "You have successfully logged in!")
        return reverse_lazy("home")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, "You have successfully logged out!")
        return super().dispatch(request, *args, **kwargs)


def test_error(request):
    """Вызывает ошибку тестирования для Rollbar."""
    a = None
    a.hello()
    return HttpResponse("This will not be reached")
