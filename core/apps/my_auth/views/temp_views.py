import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.my_auth.forms import LoginUserForm, RegisterUserForm

User = get_user_model()
logger = logging.getLogger(__name__)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = "my_auth/auth.html"
    extra_context = {"title": "Авторизация", "button_name": "Войти"}
    success_url = reverse_lazy("device:home")


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "my_auth/auth.html"
    extra_context = {"title": "Регистрация", "button_name": "Ok"}
    success_url = reverse_lazy("my_auth:login")


class MyLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
