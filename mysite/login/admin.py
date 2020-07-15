from django.contrib import admin
from .models import Cost_category,Personal_cost_category, Cost_system1, Personal_income_category, \
    Income_category,Income_system

admin.site.register(Cost_category)
admin.site.register(Personal_cost_category)
admin.site.register(Cost_system1)
admin.site.register(Personal_income_category)
admin.site.register(Income_category)
admin.site.register(Income_system)
