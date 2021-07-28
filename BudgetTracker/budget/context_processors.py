from django.conf import settings
from .models import Budget, Transaction
from django.contrib.auth.models import User



def has_budget(request):
   try:
      user = User.objects.get(username=request.user.username)
      if user:
         budget = Budget.objects.filter(user=user.id)
         return {
            'has_budget':bool(budget),
         }
   except:
      return {
         'has_budget':False,
      }


def has_transactions(request):
   try:
      user = User.objects.get(username=request.user.username)
      if user:
         transactions = Transaction.objects.filter(user=user.id)
         return {
            'has_transactions':bool(transactions),
         }
   except:
      return {
         'has_transactions':False,
      }