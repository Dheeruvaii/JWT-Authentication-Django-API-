from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import UserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations=True
    """
        This is custom user manager
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is mandatory.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is mandatory.")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """this is my custom myUser subclass of Abstractbaseuser"""
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email