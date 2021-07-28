from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import AddTransactionForm, EditBudgetForm
from django.contrib import messages
from .models import Budget, Category, Transaction
import datetime
import json


def index(request):
    if request.method == "GET":
        if 'created' in request.GET:
            messages.success(request, ("You're account has been created!"))
            return render(request, 'budget/home.html')
        elif request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            user_transactions = Transaction.objects.filter(user=user.pk)
            
            # Fetching data for Pie Chart
            category_totals = {}
            for trx in user_transactions:
                category = trx.category.category
                amount_spent = trx.amount_spent 
                if category in category_totals:
                    category_totals[category] += amount_spent
                else:
                    category_totals[category] = amount_spent
            pie_transactions = [['Category', 'Amount Spent']]
            for k,v in category_totals.items():
                pie_transactions.append([k,v])
            pie_transactions = json.dumps(pie_transactions)
            
            # Fetching data for Table Chart
            table_transactions = [['Transaction Date', 'Category', 'Amount Spent']]
            for trx in user_transactions:
                table_transactions.append([trx.transaction_date, 
                                    trx.category.category,
                                    trx.amount_spent])
            table_transactions = json.dumps(table_transactions, indent=4, sort_keys=True, default=str)

            # Fetching user's remaining allowance
            budgets = Budget.objects.filter(user=user.id)
            total_allowance = 0
            budgets_dict = {}
            for budget in budgets:
                budget_category = Category.objects.filter(budget=budget)
                category = budget_category.first()
                allowance = budget.allowance
                total_allowance+=budget.allowance
                budgets_dict[category] = allowance
            user_transactions = Transaction.objects.filter(user=user)
            user_transaction_total = 0
            for transaction in user_transactions:
                user_transaction_total+=transaction.amount_spent
            if (total_allowance < user_transaction_total):
                budget_message = "You are over your budget."
            elif (total_allowance > user_transaction_total):
                budget_message = "Total remaining allowance."
            else:
                budget_message = None
            remaining_allowance = total_allowance - user_transaction_total
            remaining_allowance = f'${round(remaining_allowance, 2)}'

            budget_bars = {}
            for k,v in budgets_dict.items():
                k=str(k)
                budget_bars[k] = {'allowance' : 0}
                budget_bars[k]['allowance'] = v
            for k,v in category_totals.items():
                k=str(k)
                budget_bars[k]['spent'] = v  
            # print(budget_bars)

            spent_percentages = {}
            for k,v in budget_bars.items():
                # print(k,v)
                try:
                    percentage_spent = (v['spent']/v['allowance'])*100
                    spent_percentages[k] = {'percentage_spent' : 0}
                    spent_percentages[k]['percentage_spent'] = percentage_spent
                    spent_percentages[k]['allowance'] = v['allowance']
                    spent_percentages[k]['spent'] = v['spent']
                except KeyError:
                    spent_percentages[k] = {'percentage_spent' : 0}
                    spent_percentages[k]['allowance'] = v['allowance']

            # Fetching data for Bar Charts
            return render(request, 'budget/home.html', {
                                    'spent_percentages' : spent_percentages,
                                    'budget_bars' : budget_bars,
                                    'pie_data' : pie_transactions,
                                    'user_transactions' : user_transactions,
                                    'table_data' : table_transactions,
                                    'remaining_allowance' : remaining_allowance,
                                    'budget_message' : budget_message,
                                    'category_totals' : category_totals })
        else:
            return render(request, 'budget/home.html')

def edit_budget(request):
    if request.method == "GET":
        edit_budget_form = EditBudgetForm()
        user = User.objects.get(pk=request.user.pk)
        categories = []
        budgets = Budget.objects.filter(user=user)
        for budget in budgets:
            for cat in budget.categories.all():
                categories.append(str(cat))
    return render(request, 'budget/edit_budget.html', {'edit_budget_form':edit_budget_form, 
                                                       'categories': categories})

def add_categories(request):
    if request.method == "POST":
        new_categories = request.POST.getlist('category')
        for category in new_categories:
            # if category doesn't exist in Category table, add category
            if not Category.objects.filter(category=category).exists(): 
                    new_category = Category(category=category)
                    new_category.save()
            # if category exists in Category table
            budget_category = Category.objects.get(category=category)
            # if user already has category in Budget table, throw error
            user = User.objects.get(pk=request.user.pk)
            users_budget = Budget.objects.filter(user=user)
            category_in_users_budget = users_budget.filter(categories=budget_category).exists()
            if category_in_users_budget:
                messages.error(request, (f"{category} already exists in your budget, please adjust your allowance or remove category instead."))
                return redirect('edit_budget')
        return render(request, 'budget/add_allowances.html', {'categories': new_categories})
    else:
        return redirect('edit_budget')

def add_allowances(request):
    if request.method == "POST":
        for k,v in request.POST.items():
            if 'csrf' not in k:
                    user = User.objects.get(pk=request.user.pk)
                    budget = Budget(user=user, allowance=v)
                    budget.save()
                    category = Category.objects.get(category=k)
                    budget.categories.add(category)
        return redirect('home')
    else: 
        return redirect('edit_budget')

def adjust_allowance(request):
    pass

def remove_categories(request):
    pass

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
    return render(request, 'budget/add_transaction.html', {'form': form,})