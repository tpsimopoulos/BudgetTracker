from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def login_user(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        if 'password' in request.POST:
            password = request.POST['password']
        else:
            password = request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Incorrect username or password provided."
            return render(request, 'authenticate/login.html', {'error_message':error_message})
    elif 'password_reset' in kwargs:
        if kwargs['password_reset'] == "True":
            password_reset_message = "Your password has been successfully reset!"
            return render(request, 'authenticate/login.html', {'password_reset_message':password_reset_message})
    else:    
        return render(request, 'authenticate/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('login_user')

def create_account(request):
    created = False
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login_user(request)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account_creation/create_account.html', {'form': form})

def reset_password(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.get(username=username):
            password = request.POST['password']
            password_confirmation = request.POST['password_confirmation']
            user = User.objects.get(username=username)
            if user.check_password(password):
                return redirect(reverse('reset_password', kwargs={'new_pass_same_as_old':True}))
            else:
                if password == password_confirmation:
                    user.set_password(password)
                    user.save()
                    return redirect(reverse('login_user', kwargs={'password_reset':True}))
                else: 
                    error_message = "Passwords don't match."
                    return render(request, 'password_recovery/reset_password.html', {'error_message':error_message})
    elif 'new_pass_same_as_old' in kwargs:
        if kwargs['new_pass_same_as_old'] == "True":
            error_message = "New password can\'t be the same as current password."
            return render(request, 'password_recovery/reset_password.html', {'error_message':error_message})
    else:
        return render(request, 'password_recovery/reset_password.html')