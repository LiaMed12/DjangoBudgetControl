# Generated by Django 3.0.6 on 2020-05-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20200527_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_cost_category',
            name='person_category_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]