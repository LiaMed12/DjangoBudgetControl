from datetime import date, timedelta

import psycopg2

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import Personal_cost_category_forms, Cost, Time, Personal_income_category, Income
from .models import Cost_system1, Personal_cost_category, Income_system

conn = psycopg2.connect(database="django3", user="postgres",
                        password="postgres", host="localhost", port=5432)


def add_pers_cost(request):
    form = Personal_cost_category_forms(request.POST)
    form2 = Personal_cost_category.objects.filter(user_login_id=request.user.username)
    exp = None
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            if post.person_category_name == None:
                exp = '0'
                return render(request, 'login/add.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("SELECT person_category_name FROM login_personal_cost_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, post.person_category_name])
                o = cur.fetchall()
                if len(o) == 0:
                    post.user_login_id = request.user.username
                    post.save()
                    return redirect('activated_account$')
                else:
                    exp = '1'
                    return render(request, 'login/add.html', assembly(exp, form, form2))
    else:
        return render(request, 'login/add.html', assembly(exp, form, form2))


def assembly(num, form, form2):
    if num == None:
        context = {
            'form': form,
            'form2': form2,
            'ex': 'Ok'

        }
    else:
        context = {
            'form': form,
            'form2': form2,
            'exp': num,
            'ex': 'Ok'
        }
    return context


def rem_pers_cost(request):
    form = Personal_cost_category_forms(request.POST)
    form2 = Personal_cost_category.objects.filter(user_login_id=request.user.username)
    exp = None
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            if post.person_category_name == None:
                exp = '0'
                return render(request, 'login/removePersonalCatForCost.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("DELETE FROM login_personal_cost_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, form.save(commit=False).person_category_name])
                conn.commit()
                return redirect('activated_account$')
    else:
        return render(request, 'login/removePersonalCatForCost.html', assembly(exp, form, form2))


def add_cost(request):
    form = Cost()
    form2 = Personal_cost_category.objects.filter(user_login_id=request.user.username)
    exp = None
    if request.method == "POST":
        form = Cost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.id_category_cost_id == None and post.id_personal_category_cost == None:
                exp = '0'
                return render(request, 'login/addCost.html', assembly(exp, form, form2))
            elif post.id_category_cost_id != None and post.id_personal_category_cost != None:
                exp = '1'
                return render(request, 'login/addCost.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("SELECT person_category_name FROM login_personal_cost_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, post.id_personal_category_cost])
                o = cur.fetchall()

                cur.execute("SELECT category_name FROM login_cost_category WHERE "
                            "category_name = %s",
                            [post.id_category_cost_id])
                c = cur.fetchall()
                if len(o) != 0:
                    post.id_personal_category_cost = o[0][0]
                    post.login_id = request.user.username
                    post.save()
                    conn.commit()
                    return redirect('activated_account$')
                elif len(c) != 0:
                    print(c[0][0])
                    post.id_category_cost_id = c[0][0]
                    post.login_id = request.user.username
                    post.save()
                    conn.commit()
                    return redirect('activated_account$')
                else:
                    exp = '-1'
                    return render(request, 'login/addCost.html', assembly(exp, form, form2))
    else:
        return render(request, 'login/addCost.html', assembly(exp, form, form2))


def cost_system(request):
    userStart = Cost_system1.objects.filter(login_id=request.user.username).order_by('date').reverse()
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    cur = conn.cursor()
    cur.execute(
        "SELECT date ,COUNT('id') FROM login_cost_system1 WHERE login_id=%s AND date BETWEEN %s AND %s GROUP BY date ORDER BY date ASC",
        [request.user.username, start_date, end_date])
    o = cur.fetchall()

    context = {
        'posts': userStart,
        'values': o,
        'ex': 'Ok'

    }
    if request.method == "POST":
        form = Time(request.POST)
        if form.is_valid():
            userStartnew = Cost_system1.objects.filter(login_id=request.user.username,
                                                       date__range=[form.cleaned_data['renewal_date'],
                                                                    form.cleaned_data['renewal_date2']]).order_by(
                'date').reverse()
            cur = conn.cursor()
            cur.execute(
                "SELECT date ,COUNT('id') FROM login_cost_system1 WHERE login_id=%s AND date >= %s AND date<= %s GROUP BY date ORDER BY date",
                [request.user.username, form.cleaned_data['renewal_date'], form.cleaned_data['renewal_date2']])
            o = cur.fetchall()
            context = {
                'posts': userStartnew,
                'values': o,
                'ex': 'Ok'

            }
            return render(request, 'login/Cost_system.html', context)

    else:
        form = Time()
    return render(request, 'login/Cost_system.html', context)
