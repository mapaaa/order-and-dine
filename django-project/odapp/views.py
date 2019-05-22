from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm 
from django.shortcuts import redirect, render
from odapp.admin import UserCreationForm
from odapp.settings import AuthenticationBackend


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='odapp.settings.AuthenticationBackend')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'odapp/signup.html', {'form': form})


def index(request):
    return render(request, 'odapp/index.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user, backend='odapp.settings.AuthenticationBackend')
            return redirect('/')
        return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'odapp/login.html', {'form' : form})
