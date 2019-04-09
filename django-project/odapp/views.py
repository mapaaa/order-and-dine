from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from odapp.admin import UserCreationForm


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
