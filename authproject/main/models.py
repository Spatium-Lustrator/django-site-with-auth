from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_login = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=20)
    user_gender = models.BooleanField(default=False)
    user_postcode = models.IntegerField(default=False)
    user_phone_number = models.IntegerField(default=False)
    user_balance = models.IntegerField(default=False)
    user_password = models.CharField(max_length=20)

    def __str__(self):
        return self.field_name