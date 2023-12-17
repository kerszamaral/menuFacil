from django.urls import path, include

from . import views

app_name = 'account'
urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("", include("django.contrib.auth.urls")),
    path("", views.index, name="profile"),
    path("<int:pk>/delete", views.UserDelete.as_view(), name="delete"),
    path("logout", views.logout_view, name="logout")
]
