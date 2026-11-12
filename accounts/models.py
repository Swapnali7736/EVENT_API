from django.db import models

from django.contrib.auth.models import AbstractUser
class MyUser(AbstractUser):
    role_choices=[
        ('organizer', 'Organizer'),
        ('customer', 'Customer'),
        ]
    role = models.CharField(max_length=20,choices=role_choices)
    phone = models.CharField(max_length=15, null=True)