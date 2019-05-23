from django import forms
import datetime


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ReservationForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    date = forms.DateField(initial=datetime.date.today)
    time = forms.TimeField()
    number_of_people = forms.IntegerField(min_value=1, max_value=5)
