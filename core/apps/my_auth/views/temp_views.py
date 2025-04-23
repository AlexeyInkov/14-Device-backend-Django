import json
import logging
import secrets

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView
from django_telegram_login.widgets.constants import MEDIUM
from django_telegram_login.widgets.generator import create_redirect_login_widget, create_callback_login_widget
from requests import Response

from apps.my_auth.forms import LoginUserForm, RegisterUserForm
from apps.my_auth.models import Profile

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
