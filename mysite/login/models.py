
import psycopg2
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Cost_category(models.Model):
    category_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.category_name

class Personal_cost_category(models.Model):
    person_category_name = models.CharField(max_length=50, blank=True, null=True)
    user_login = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)

class Cost_system1(models.Model):
    date = models.DateField(default=timezone.now)
    sum = models.DecimalField(max_digits=20, decimal_places=2)
    login = models.ForeignKey(User, to_field='username', max_length=50, on_delete=models.CASCADE)
    id_category_cost = models.ForeignKey(Cost_category, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    id_personal_category_cost = models.CharField(max_length=50, blank=True, null=True)

class Income_category(models.Model):
    category_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.category_name

class Personal_income_category(models.Model):
    person_category_name = models.CharField(max_length=50,blank=True, null=True)
    user_login = models.ForeignKey(User,to_field='username', on_delete=models.CASCADE)

class Income_system(models.Model):
    date = models.DateField(default=timezone.now)
    sum = models.DecimalField(max_digits=20, decimal_places=2)
    login = models.ForeignKey(User, to_field='username', max_length=50,on_delete=models.CASCADE)
    id_category_income = models.ForeignKey(Income_category, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    id_personal_category_income = models.CharField(max_length=50, blank=True, null=True)







