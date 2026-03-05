from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", views.HomeView.as_view(), name="home"),
    path("users/", include("task_manager.users.urls")),
    path("statuses/", include("task_manager.statuses.urls")),
    path("tasks/", include("task_manager.tasks.urls")),
    path("labels/", include("task_manager.labels.urls")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
]
