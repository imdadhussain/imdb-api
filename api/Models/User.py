from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from api.helpers.media_helper import get_media_url

from django.db import models


class BaseAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            **extra_fields

        )
        user.is_staff = True
        permissions = Permission.objects.filter()
        user.user_permissions.add(*permissions)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseAbstract):
    """
    User model : Table for Movies
    """
    name = models.CharField(max_length=200, default=str(), blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True, db_index=True)
    dob = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or str()

    def json(self, request=None):
        res = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'dob': self.dob.strftime('%d-%m-%Y'),
            'avatar': get_media_url(request, str(self.avatar)) if self.avatar else '',
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'is_admin': self.is_staff
        }
        return res
