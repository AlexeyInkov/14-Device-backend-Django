from django.shortcuts import render


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
