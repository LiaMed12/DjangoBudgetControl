from datetime import datetime, date, timedelta

import psycopg2
from django.http import HttpRequest

from .forms import Personal_cost_category_forms, Personal_income_category_forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import Time, Personal_income_category, Income
from .models import Income_system

conn = psycopg2.connect(database="django3", user="postgres",
                        password="postgres", host="localhost", port=5432)

def add_pers_inc(request):
    form = Personal_income_category_forms(request.POST)
    form2 = Personal_income_category.objects.filter(user_login_id=request.user.username)
    exp = None
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            if post.person_category_name ==None:
                exp = '0'
                return render(request, 'login/addIncPers.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("SELECT person_category_name FROM login_personal_income_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, post.person_category_name])
                o = cur.fetchall()
                if len(o) == 0 and o != None:
                    post.user_login_id = request.user.username
                    post.save()
                    return redirect('activated_account$')
                else:
                    exp = '1'
                    return render(request, 'login/addIncPers.html', assembly(exp, form, form2))
    else:
        return render(request, 'login/addIncPers.html', assembly(exp,form,form2))

def assembly(num, form, form2):
    if num == None:
        context = {
            'form': form,
            'form2': form2,
        }
    else:
        context = {
            'form': form,
            'form2': form2,
            'exp': num
        }
    return context


def rem_pers_inc(request):
    form = Personal_income_category_forms(request.POST)
    form2 = Personal_income_category.objects.filter(user_login_id=request.user.username)
    exp = None
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            if post.person_category_name == None:
                exp = '0'
                return render(request, 'login/removePersonalCatForInc.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("DELETE FROM login_personal_income_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, form.save(commit=False).person_category_name])
                conn.commit()
                return redirect('activated_account$')
    else:
        return render(request, 'login/removePersonalCatForInc.html', assembly(exp, form,form2))


def add_income(request):
    form = Income()
    form2 = Personal_income_category.objects.filter(user_login_id=request.user.username)
    exp =None
    if request.method == "POST":
        form = Income(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if post.id_personal_category_income == None and post.id_category_income_id == None:
                exp = '0'
                return render(request, 'login/addInc.html', assembly(exp, form, form2))
            elif post.id_personal_category_income != None and post.id_category_income_id != None:
                exp = '1'
                return render(request, 'login/addInc.html', assembly(exp, form, form2))
            else:
                cur = conn.cursor()
                cur.execute("SELECT person_category_name FROM login_personal_income_category WHERE "
                            "user_login_id = %s AND person_category_name = %s",
                            [request.user.username, post.id_personal_category_income])
                o = cur.fetchall()

                cur.execute("SELECT category_name FROM login_income_category WHERE "
                            "category_name = %s",
                            [post.id_category_income_id])
                c = cur.fetchall()
                if len(o) != 0:
                    post.id_personal_category_income = o[0][0]
                    post.login_id = request.user.username
                    post.save()
                    conn.commit()
                    return redirect('activated_account$')
                elif len(c) != 0:
                    print(c[0][0])
                    post.id_category_income_id = c[0][0]
                    post.login_id = request.user.username
                    post.save()
                    conn.commit()
                    return redirect('activated_account$')
                else:
                    exp = '-1'
                    return render(request, 'login/addInc.html', assembly(exp, form, form2))
    else:
      return render(request, 'login/addInc.html', assembly(exp, form, form2))


def income_system(request):
    userStart = Income_system.objects.filter(login_id=request.user.username).order_by('date').reverse()
    cur = conn.cursor()
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    cur.execute(
        "SELECT date ,COUNT('id') FROM login_income_system WHERE login_id=%s AND date >= %s GROUP BY date ORDER BY date",
        [request.user.username, start_date])
    o = cur.fetchall()
    context = {
        'posts': userStart,
        'values': o
    }
    if request.method == "POST":
        form = Time(request.POST)
        if form.is_valid():
            userStartnew = Income_system.objects.filter(login_id=request.user.username,
                                                        date__range=[form.cleaned_data['renewal_date'],
                                                                     form.cleaned_data['renewal_date2']])
            cur = conn.cursor()
            cur.execute(
                "SELECT date ,COUNT('id') FROM login_cost_system1 WHERE login_id=%s AND date >= %s AND date<= %s GROUP BY date ORDER BY date",
                [request.user.username, form.cleaned_data['renewal_date'], form.cleaned_data['renewal_date2']])
            o = cur.fetchall()
            context = {
                'posts': userStartnew,
                'values': o
            }
            return render(request, 'login/Income_system.html', context)

    else:
        form = Time()
    return render(request, 'login/Income_system.html', context)