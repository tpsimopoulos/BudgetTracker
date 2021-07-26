from django.conf import settings
from .models import Budget
from django.contrib.auth.models import User


def has_budget(request):
    user = User.objects.get(username=request.user.username)
    budgets = Budget.objects.filter(user=user.id)
    return {
       'has_budget':bool(budgets),
    }