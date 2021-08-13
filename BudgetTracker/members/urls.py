from django.urls import path
from . import views


urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('login_user/<str:password_reset>', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('create_account', views.create_account, name='create_account'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('reset_password/<str:new_pass_same_as_old>', views.reset_password, name='reset_password'),
]