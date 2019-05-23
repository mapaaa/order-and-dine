from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.shortcuts import redirect, render, get_object_or_404
from odapp.admin import UserCreationForm
from odapp.settings import AuthenticationBackend
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .models import Restaurant
from .forms import ContactForm, ReservationForm, OrderForm
from django.conf import settings
import random


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


def index2(request, action):
    if request.user.is_authenticated:
        restaurants = Restaurant.objects.order_by('-name')
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'odapp/index.html', {'restaurants' : restaurants, 'action': action})


def index(request):
    action = 'False'
    if request.user.is_authenticated:
        restaurants = Restaurant.objects.order_by('-name')
    else:
        restaurants = Restaurant.objects.all()
    return render(request, 'odapp/index.html', {'restaurants' : restaurants, 'action': action})


def restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'odapp/restaurant.html', {'restaurant' : restaurant})


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
        if form.is_valid():
            full_name = form.cleaned_data['full_name']  
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail('ORDER_AND_DINE', email + ' ' + full_name + '\n' + message, settings.EMAIL_HOST_USER, ['cllaire11@gmail.com '], False)
                send_mail('Order and Dine Services', 'Thank you for contacting Order and Dine!\n\nWe will respond to your inquiry as soon as possible within the next two business days. \nBe sure to add orderanddine@yahoo.com to your address book or safe sender list to ensure that you receive our e-mails.\n\nBon Appetit,\nOrder and Dine Team', settings.EMAIL_HOST_USER, [email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, 'odapp/contact.html', {'form' : form})


def success(request):
    return render(request, 'odapp/success.html')


def logout_view(request):
    logout(request)         
    return redirect('index2',  action='LoggedOut')


def reservation(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'GET':
        form = ReservationForm()
    else:
        form = ReservationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']  
            email = form.cleaned_data['email']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            number_of_people = form.cleaned_data['number_of_people']
            try:
                send_mail('Reservation request', full_name + ' ' + email + ' ' + str(date) + ' ' + str(time) + ' ' +  ' ' + str(number_of_people) + restaurant.name, settings.EMAIL_HOST_USER, ['cllaire11@gmail.com' ], False)
                send_mail('Order and Dine Services', 'Thank you for making a reservation at ' + restaurant.name + '!\n\nWe will confirm your reservation as soon as possible.\nBe sure to add orderanddine@yahoo.com to your address book or safe sender list to ensure that you receive our e-mails.\n\nBon Appetit,\nOrder and Dine Team', settings.EMAIL_HOST_USER, [email], False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('index2', action='ReservationMade')
    return render(request, 'odapp/reservation.html', {'form' : form, 'restaurant': restaurant})


def restaurant(request, pk):
    if request.method == 'POST':
        return redirect('index2', action='OrderPlaced')
    else:
        restaurant = get_object_or_404(Restaurant, pk=pk)
        form = OrderForm()
        print(form)
        return render(request, 'odapp/restaurant.html', {'restaurant' : restaurant, 'form': form})
