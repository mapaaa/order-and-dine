from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    from_email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
