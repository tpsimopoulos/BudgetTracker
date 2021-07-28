from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('add_categories', views.add_categories, name='add_categories'),
    path('add_allowances', views.add_allowances, name='add_allowances'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
    path('edit_budget', views.edit_budget, name='edit_budget'),
    path('edit_budget/adjust_allowance', views.adjust_allowance, name='adjust_allowance'),
    path('edit_budget/save_allowance_adjustments', views.save_allowance_adjustments, name='save_allowance_adjustments'),
    path('edit_budget/remove_categories', views.remove_categories, name='remove_categories'),
]