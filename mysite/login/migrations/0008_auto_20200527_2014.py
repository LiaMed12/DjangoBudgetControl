# Generated by Django 3.0.6 on 2020-05-27 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20200527_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost_system1',
            name='date',
            field=models.DateField(default=datetime.date(2010, 3, 14)),
        ),
    ]