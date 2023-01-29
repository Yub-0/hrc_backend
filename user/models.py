from django.db import models
from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phone:
            raise ValueError(_('The Phone number must be set'))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Others')
    )
    USER_STATUS = (
        (1, 'Active'),
        (2, 'Inactive')
    )
    phone = PhoneNumberField(unique=True)
    name = models.CharField(null=False, blank=False, max_length=25)
    status = models.IntegerField(choices=USER_STATUS, default=1)
    date_joined = models.DateField(default=date.today)
    birthdate = models.DateField(auto_now=False, default=date.today)
    gender = models.IntegerField(choices=GENDER, default=1)
    image = models.ImageField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'role']
    USERNAME_FIELD = 'phone'

    objects = CustomUserManager()

    def __str__(self):
        return self.name