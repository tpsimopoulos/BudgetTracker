from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('create_budget', views.create_budget, name='create_budget'),
    path('add_transaction', views.add_transaction, name='add_transaction'),
]