from audioop import reverse

from django.contrib.auth.decorators import login_required

from .viewsCost import *
from .viewsIncome import *

from datetime import datetime

import psycopg2
from django.http import HttpRequest, HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


conn = psycopg2.connect(database="django3", user="postgres",
                        password="postgres", host="localhost", port=5432)

def index(request):
    list_articles = User
    context = {'name': list_articles}
    template = 'login/mainHome.html'
    return render(request, template, context)


def detail_page(request):
    template = 'login/registration/login.html'
    return render(request, template)


def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            # переадресация на главную страницу после регистрации

            return render(request, 'login/mainHome.html')
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных нового пользователя
        assert isinstance(request, HttpRequest)
    return render(
        request,
        'login/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def activated(request):
    user = User.objects.get(username=request.user.username)
    context = {'name': user,
               'ex' : 'Ok' }
    template = 'login/mainHomeAuto.html'
    return render(request, template, context)





