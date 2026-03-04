
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", views.HomeView.as_view(), name="home"),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("tasks/", include("tasks.urls")),
    path("labels/", include("labels.urls")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]
