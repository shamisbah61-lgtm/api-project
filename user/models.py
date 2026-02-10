from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True,max_length=255,error_messages={"unique": "Email already exists."})
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    objects = UserManager()


class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']

        def __str__(self):
            return self.email



