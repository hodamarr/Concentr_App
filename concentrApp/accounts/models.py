from django.db import models
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault(
            "is_staff", True
        )
        extra_fields.setdefault(
            "is_superuser", True
        )
        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser is_staff attribute should be true")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser is_superuser attribute should be true")
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=20)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
