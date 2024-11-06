from django.shortcuts import render


def index(request):
    data = {
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_tso(request, tso_id):
    data = {
        'title': 'Отображение по ТСО',
        'tso_selected': tso_id,
    }
    return render(request, 'frontend/index.html', context=data)


def show_customers(request, tso_id, customer_id):
    data = {
        'title': 'Отображение по ТСО',
        'tso_selected': tso_id,
        'customer_selected': customer_id,
    }
    return render(request, 'frontend/index.html', context=data)