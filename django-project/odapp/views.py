from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from odapp.admin import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'odapp/signup.html', {'form': form})


def index(request):
    return render(request, 'odapp/index.html')
