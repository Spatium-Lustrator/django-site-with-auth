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

class CurrentState(models.Model):
    id = models.IntegerField(primary_key = True)
    basic_state = models.BooleanField(default=True)
    federal_state = models.BooleanField(default=False)
    

class BasicVote(models.Model):
    region_id = models.OneToOneField('Region', primary_key=True, on_delete=models.CASCADE)
    big_region_id = models.IntegerField()
    count_of_votes = models.IntegerField()

class FederalVote(models.Model):
    region_id = models.OneToOneField('Region', primary_key=True, on_delete=models.CASCADE)
    count_of_votes = models.IntegerField()

class TrailVote(models.Model):
    trail_id = models.OneToOneField('Trail', primary_key=True, on_delete=models.CASCADE)
    count_of_votes = models.IntegerField()

class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=200)

class BigRegion(models.Model):
    big_region_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=200)

class Trail(models.Model):
    trail_id = models.IntegerField(primary_key=True),
    trail_title = models.TextField(max_length=40)
    trail_preview = models.TextField(max_length=1000)
    trail_description = models.TextField(max_length=500)
    trail_is_on_vote = models.BooleanField()
    # trail_votes = models.ForeignKey(User, on_delete=models.CASCADE)

