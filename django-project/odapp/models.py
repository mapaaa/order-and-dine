from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
            verbose_name='email address',
            max_length = 1000,
            unique = True,
    )
    preferences = models.ManyToManyField('FoodTag')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
       return self.email


class FoodTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

