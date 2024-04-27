from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

# Create your models here.
class User(AbstractUser, PermissionsMixin):
    user_login = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=20)
    user_gender = models.BooleanField(default=False)
    user_postcode = models.IntegerField(default=False)
    user_phone_number = models.IntegerField(default=False)
    user_balance = models.IntegerField(default=False)
