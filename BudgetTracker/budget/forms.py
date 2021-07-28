from django import forms
from .models import Category, Transaction, Budget
from django.contrib.auth.models import User
from django.forms import ModelForm, formset_factory


class CategoriesForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(
                        queryset=Category.objects.all(),
                        to_field_name="category",
                        widget=forms.SelectMultiple(
                            attrs={'class':'selectpicker form-control',
                            'multiple data-live-search':'true',
                            })
                        )
# class AllowanceForm(forms.Form):
#     allowance = forms.IntegerField(widget=forms.NumberInput(
#                                 attrs={'class':'form-control'}
#                         ))

# class AddCategoryForm(forms.Form):
#     category = forms.CharField(strip=True) 

# AddCategoryFormSet = formset_factory(AddCategoryForm)

class EditBudgetForm(forms.Form):
    CHOICES = [
        ('Add Category', 'Add Category'),
        ('Adjust Allowance', 'Adjust Allowance'),
        ('Remove Tracked Category', 'Remove Tracked Category')
    ]
    actions = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={}))

class CustomDateInput(forms.DateInput):
    input_type = 'date'

class AddTransactionForm(ModelForm):
    class Meta: 
        model = Transaction
        fields = ['category', 'transaction_date', 'amount_spent']
        widgets = {'transaction_date' : CustomDateInput()}
