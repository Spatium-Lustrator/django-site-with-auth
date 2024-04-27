from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=20, primary_key=True)
    user_login = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=20)
    user_password = models.CharField(max_length=20)

    def __str__(self):
        return self.field_name


class Votes(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    votes = models.IntegerField()
    donates = models.FloatField()