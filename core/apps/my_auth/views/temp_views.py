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


class MyLoginTelegramView(TemplateView):
    def get(self, request, *args, **kwargs):
        bot_name = settings.TELEGRAM_BOT_NAME
        unique_token = secrets.token_urlsafe()
        cache.set(unique_token, unique_token, timeout=300)
        # telegram_login_widget = create_redirect_login_widget(redirect(
        #     "my_auth:telegram_redirect"),
        #     bot_name,
        #     size=MEDIUM
        # )
        telegram_login_widget = create_callback_login_widget(bot_name, unique_token)
        context = {
            "telegram_login_widget": telegram_login_widget,
            "bot_name": bot_name,
            "unique_token": unique_token,
        }
        return render(request, "my_auth/redirect.html", context)


@csrf_exempt
def telegram_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        telegram_username = data.get("telegram_username")
        auth_token = data.get("auth_token")
        session_token = cache.get(auth_token)
        if auth_token != session_token:
            logger.debug(f"Invalid token {auth_token} != {session_token}")
            return Response(error={"error": "Invalid token"}, status=400)
        cache.delete(auth_token)

        user, created = get_user_model().objects.get_or_create(
            username=telegram_username
        )
        if created:
            if data.get("telegram_first_name"):
                user.first_name = data.get("telegram_first_name")
            if data.get("telegram_last_name"):
                user.last_name = data.get("telegram_last_name")
            user.save()
            profile = Profile.objects.create(user=user, telegram_id=data.get("telegram_id"))
            profile.save()

        login(request, user)
        return redirect("device:home")

# def index(request):
#
#     # Initially, the index page may have no get params in URL
#     # For example, if it is a home page, a user should be redirected from the widget
#     if not request.GET.get('hash'):
#         return HttpResponse('Handle the missing Telegram data in the response.')
#
#     try:
#         result = verify_telegram_authentication(
#             bot_token=bot_token, request_data=request.GET
#         )
#
#     except TelegramDataIsOutdatedError:
#         return HttpResponse('Authentication was received more than a day ago.')
#
#     except NotTelegramDataError:
#         return HttpResponse('The data is not related to Telegram!')
#
#     # Or handle it like you want. For example, save to DB. :)
#     return HttpResponse('Hello, ' + result['first_name'] + '!')
#
#
# def callback(request):
#     telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)
#
#     context = {'telegram_login_widget': telegram_login_widget}
#     return render(request, 'my_auth/callback.html', context)
#
#
# def redirect(request):
#     telegram_login_widget = create_redirect_login_widget(
#         redirect_url, bot_name, size=LARGE, user_photo=DISABLE_USER_PHOTO
#     )
#
#     context = {'telegram_login_widget': telegram_login_widget}
#     return render(request, 'my_auth/redirect.html', context)
