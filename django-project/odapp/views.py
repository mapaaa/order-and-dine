from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm 
from django.shortcuts import redirect, render
from odapp.admin import UserCreationForm
from odapp.settings import AuthenticationBackend
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .models import Restaurant
from .forms import ContactForm
from django.conf import settings


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
    restaurants = Restaurant.objects.all()
    print(len(restaurants))
    return render(request, 'odapp/index.html', {'restaurants' : restaurants})


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


def about(request):
    return render(request, 'odapp/about.html')


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        print(form.is_valid)
        if form.is_valid():
            print('isva;i')
            full_name = form.cleaned_data['full_name']  
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail('ORDER_AND_DINE', from_email + ' ' + full_name + '\n' + message, settings.EMAIL_HOST_USER, ['maria.pandele33@gmail.com'], False)
                send_mail('Order and Dine Services', 'Thank you for contacting Order and Dine!\n\nWe will respond to your inquiry as soon as possible within the next two business days. \nBe sure to add orderanddine@yahoo.com to your address book or safe sender list to ensure that you receive our e-mails.\n\nBon Appetit,\nOrder and Dine Team', settings.EMAIL_HOST_USER, [from_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'odapp/contact.html', {'form' : form})


def success(request):
    return render(request, 'odapp/success.html')
