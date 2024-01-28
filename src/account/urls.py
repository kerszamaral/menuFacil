from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("change/", auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:logout')), name="password_change"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("", views.index, name="profile"),
    path("<int:pk>/delete", views.UserDelete.as_view(), name="delete"),
    path("logout/", views.logout_view, name="logout"),
    path("change_done/", views.logout_view, name="password_change_done"),
]
