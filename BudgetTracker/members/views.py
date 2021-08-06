from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def login_user(request):
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
            messages.error(request, ("Incorrect username or password provided."))
            return redirect('login')
    else:
        if 'password_reset' in request.GET:
            messages.success(request, ("Password successfully reset!"))
        return render(request, 'authenticate/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out."))
    return redirect('login')

def create_account(request):
    created = False
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login_user(request)
            return redirect(reverse('home') + '?created=True')
    else:
        form = UserCreationForm()
    return render(request, 'account_creation/create_account.html', {'form': form})

def reset_password(request):
    if request.method == "POST":
        username = request.POST['username']
        if User.objects.get(username=username):
            password = request.POST['password']
            password_confirmation = request.POST['password_confirmation']
            user = User.objects.get(username=username)
            if user.check_password(password):
                return redirect(reverse('reset_password') + '?new_pass_same_as_old=True')
            else:
                if password == password_confirmation:
                    user.set_password(password)
                    user.save()
                    return redirect(reverse('login') + '?password_reset=True')
                else: 
                    messages.error(request, ("Passwords do not match."))
                    return redirect('reset_password')
    elif 'new_pass_same_as_old' in request.GET:
        messages.error(request, ("New password can\'t be the same as current password."))
        return redirect('reset_password')
    else:
        return render(request, 'password_recovery/reset_password.html')