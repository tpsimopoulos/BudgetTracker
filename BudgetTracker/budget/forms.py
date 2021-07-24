from django import forms
from .models import Category, Transaction
from django.forms import ModelForm


class BudgetForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
                        queryset=Category.objects.all(),
                        to_field_name="category"
                        )
    allowance = forms.IntegerField()


class CustomDateInput(forms.DateInput):
    input_type = 'date'

class AddTransactionForm(ModelForm):
    class Meta: 
        model = Transaction
        fields = ['category', 'transaction_date', 'amount_spent']
        widgets = {'transaction_date' : CustomDateInput()}