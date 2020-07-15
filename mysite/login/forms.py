from .models import Personal_cost_category, Cost_system1, Personal_income_category, Income_system
from django import forms


class Personal_cost_category_forms(forms.ModelForm):
    class Meta:
        model = Personal_cost_category
        fields = ('person_category_name',)


class Cost(forms.ModelForm):
    class Meta:
        model = Cost_system1
        fields = ('date', 'sum', 'id_category_cost', 'id_personal_category_cost',)

class Time(forms.Form):
    renewal_date = forms.DateField()
    renewal_date2 = forms.DateField()

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        return data

    def clean_renewal_date2(self):
        data = self.cleaned_data['renewal_date2']
        return data

class Personal_income_category_forms(forms.ModelForm):
    class Meta:
        model = Personal_income_category
        fields = ('person_category_name',)

class Income(forms.ModelForm):
    class Meta:
        model = Income_system
        fields = ('date', 'sum', 'id_category_income', 'id_personal_category_income',)