from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import LoginUserForm, RegisterUserForm
from .mixins import DataMixin


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'frontend/login.html'
    extra_context = {'title': 'Авторизация'}


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'frontend/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('frontend:login')


class IndexView(DataMixin, ListView):
    template_name = 'frontend/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    tso_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')


def index(request):
    data = {
        'title': 'Главная страница',
        'tso_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_tso(request, tso_id):
    data = {
        'title': 'Отображение по ТСО',
        'tso_selected': tso_id,
        'cust_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_customers(request, tso_id, customer_id):
    data = {
        'title': 'Отображение по Абоненту',
        'tso_selected': tso_id,
        'cust_selected': customer_id,
        'mu_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_metering_units(request, tso_id, customer_id, mu_id):
    data = {
        'title': 'Отображение по УУТЭ',
        'tso_selected': tso_id,
        'cust_selected': customer_id,
        'mu_selected': mu_id,
        'dev_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_devices(request, tso_id, customer_id, mu_id, dev_id):
    data = {
        'title': 'Отображение по УУТЭ',
        'tso_selected': tso_id,
        'cust_selected': customer_id,
        'mu_selected': mu_id,
        'dev_selected': dev_id,
    }
    return render(request, 'frontend/index.html', context=data)
