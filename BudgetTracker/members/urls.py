from django.urls import path
from . import views


urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('create_account', views.create_account, name='create_account'),
    path('reset_password', views.reset_password, name='reset_password'),
]