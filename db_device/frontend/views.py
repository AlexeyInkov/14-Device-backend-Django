from django.shortcuts import render


def index(request):
    data = {
        'title': 'Главная страница',
        'cat_selected': 0,
    }
    return render(request, 'frontend/index.html', context=data)


def show_organization(request, org_id):
    data = {
        'title': 'Отображение по организации',
        'org_selected': org_id,
    }
    return render(request, 'frontend/index.html', context=data)
