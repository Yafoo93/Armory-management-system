from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ArmorOfficerRegistration


def home(request):
    return render(request, 'custom_auth/home.html')


def hello(request):
    return HttpResponse("Hello, World!")


def register(request):
    if request.method == 'POST':
        form = ArmorOfficerRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = ArmorOfficerRegistration()
    return render(request, 'custom_auth/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request, 'custom_auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')
