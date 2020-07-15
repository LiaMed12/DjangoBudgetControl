# Generated by Django 3.0.6 on 2020-07-10 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20200708_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost_system1',
            name='date',
            field=models.DateField(default=datetime.date(2020, 7, 10)),
        ),
        migrations.AlterField(
            model_name='income_system',
            name='date',
            field=models.DateField(default=datetime.date(2020, 7, 10)),
        ),
        migrations.AlterField(
            model_name='personal_cost_category',
            name='person_category_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
