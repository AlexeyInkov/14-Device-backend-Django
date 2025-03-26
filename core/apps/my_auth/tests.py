import os

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.frontend.urls import urlpatterns as frontend_urls
from apps.my_auth.forms import LoginUserForm, RegisterUserForm


class LoginUserFormTestCase(TestCase):
    """Tests LoginUserForm."""

    def test_form_valid(self):
        form_data = {
            "username": os.environ.get("ADMIN_USERNAME"),
            "password": os.environ.get("ADMIN_PASSWORD"),
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {"password": os.environ.get("ADMIN_PASSWORD")}
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())


class RegisterUserFormTestCase(TestCase):
    """Tests RegisterUserForm."""

    def test_form_valid(self):
        form_data = {
            "username": "ADMIN_USERNAME",
            "email": "ADMIN_EMAIL@gmail.com",
            "password1": "ADMIN_password",
            "password2": "ADMIN_password",
        }
        form = RegisterUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        form_data = {
            "username": "ADMIN_USERNAME",
            "email": "ADMIN_EMAIL@gmail.com",
            "password1": "ADMIN_password",
        }
        form = RegisterUserForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTestCase(TestCase):

    def test_not_authentication(self):
        """
        Проверка доступности страницы пользователям, не авторизованным на сайте
        """
        for frontend_url in frontend_urls:
            if frontend_url.name in ("device_detail", "update_device_verification"):
                url = reverse(f"frontend:{frontend_url.name}", args=(1,))
            else:
                url = reverse(f"frontend:{frontend_url.name}")
            response = self.client.get(url)
            self.assertRedirects(
                response,
                reverse("my_auth:login") + "?next=" + url,
                status_code=302,
                target_status_code=200,
            )

    def test_login_view(self):
        """
        Проверка страницы входа
        """
        response = self.client.get(reverse("my_auth:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_auth/auth.html")
        response = self.client.post(
            reverse("my_auth:login"),
            {
                "username": os.environ.get("ADMIN_USERNAME"),
                "password": os.environ.get("ADMIN_PASSWORD"),
            },
        )
        self.assertRedirects(
            response, reverse("frontend:home"), status_code=302, target_status_code=200
        )
        self.assertEqual(self.client.session["_auth_user_id"], "1")

    def test_logout_view(self):
        """
        Проверка страницы выхода
        """
        response = self.client.get(reverse("my_auth:logout"))
        self.assertRedirects(
            response, reverse("my_auth:login"), 302, target_status_code=200
        )
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_register_view(self):
        """
        Проверка страницы регистрации
        """
        response = self.client.get(reverse("my_auth:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_auth/auth.html")
        """ 
        Проверка создания нового пользователя
        """
        response = self.client.post(
            reverse("my_auth:register"),
            {
                "username": "ADMIN_USERNAME",
                "email": "ADMIN_EMAIL@gmail.com",
                "password1": "ADMIN_password",
                "password2": "ADMIN_password",
            },
        )
        self.assertRedirects(
            response, reverse("my_auth:login"), status_code=302, target_status_code=200
        )
        user = User.objects.get(username="ADMIN_USERNAME")
        self.assertEqual(user.email, "ADMIN_EMAIL@gmail.com")
