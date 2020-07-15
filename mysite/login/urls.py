from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^activated_account$', views.activated, name='activated_account$'),
    path('account/', include('django.contrib.auth.urls'), name = 'login'),
    path('account/', include('django.contrib.auth.urls'), name=' logout'),
    path('cost/new/', views.add_pers_cost, name='add_pers_cost'),
    path('cost/remove/', views.rem_pers_cost, name='rem_pers_cost'),
    path('cost/costAdd/', views.add_cost, name='add_cost'),
    path('cost/cosSys/', views.cost_system, name='cost_system'),
    path('Inc/new/', views.add_pers_inc, name='add_pers_inc'),
    path('Inc/remove/', views.rem_pers_inc, name='rem_pers_inc'),
    path('Inc/incAdd/', views.add_income, name='add_income'),
    path('Inc/incSys/', views.income_system, name='income_system'),
]

