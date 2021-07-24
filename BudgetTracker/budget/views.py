from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import BudgetForm, AddTransactionForm
from django.contrib import messages
from .models import Budget, Category, Transaction
import datetime
import json


def index(request):
    if 'created' in request.GET:
        messages.success(request, ("You're account has been created!"))
    
    user = User.objects.get(username=request.user.username)
    user_transactions = Transaction.objects.filter(user=user)
    
    # Fetching data for Pie Chart
    pie_transactions = [['Category', 'Amount Spent']]
    for trx in user_transactions:
        pie_transactions.append([trx.category.category,
                                 trx.amount_spent])
    pie_transactions = json.dumps(pie_transactions)
    
    # Fetching data for Table Chart
    table_transactions = [['Transaction Date', 'Category', 'Amount Spent']]
    for trx in user_transactions:
        table_transactions.append([trx.transaction_date, 
                             trx.category.category,
                             trx.amount_spent])
    table_transactions = json.dumps(table_transactions, indent=4, sort_keys=True, default=str)
    
    return render(request, 'budget/home.html', {'user' : request.user, 
                            'pie_data' : pie_transactions,
                            'table_data' : table_transactions, })

def create_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            categories = request.POST.getlist('categories')
            allowance = request.POST['allowance']
            budget = Budget(user=user, allowance=allowance)
            budget.save()
            for category in categories:
                category = Category.objects.get(category=category)
                budget.categories.add(category)
            messages.success(request, ("You're budget has been created!"))
            return redirect('home')
    else: 
        form = BudgetForm()
    return render(request, 'budget/create_budget.html', {'form': form})

def add_transaction(request):
    if request.method == "POST":
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            category = request.POST['category']
            category = Category.objects.get(pk=category)
            transaction_date = request.POST['transaction_date']
            amount_spent = request.POST['amount_spent']
            transaction = Transaction(user=user, category=category, transaction_date=transaction_date, amount_spent=amount_spent)
            transaction.save()
            messages.success(request, ("Transaction added!"))
            return redirect('add_transaction')
    else:
        form = AddTransactionForm()
    return render(request, 'budget/add_transaction.html', {'form': form})