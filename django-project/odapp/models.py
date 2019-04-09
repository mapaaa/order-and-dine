from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core import validators
from django.utils.translation import ugettext_lazy as _



class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Usersmust have an email address.')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        print('First_name = ' + first_name)
        print('Last_name = ' + last_name)
        print('Email = ' + email)
        print('Password = ' + password)
        user=self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length = 1000,
        unique = True,
    )
    preferences = models.ManyToManyField('FoodTag')
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
       return self.email

    @property
    def is_staff(self):
        return self.is_admin


class FoodTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

