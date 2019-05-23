from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from odapp.models import CustomUser, FoodTag, Restaurant, Meniu


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'input',
        }
    ))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={
            'class': 'input',
        }
    ))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'class': 'input',
        }
    ))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'class': 'input',
        }
    ))
    email = forms.CharField(label='Email', widget=forms.EmailInput(
        attrs={
            'class': 'input',
        }
    ))
    preferences = forms.ModelMultipleChoiceField(queryset=FoodTag.objects.all(), widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': '',
        }
    ))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        user.preferences.add(*self.cleaned_data['preferences'])
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'last_name', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.register(FoodTag)
admin.site.register(Restaurant)
admin.site.register(Meniu)
admin.site.unregister(Group)

