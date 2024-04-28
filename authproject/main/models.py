from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models import ForeignKey


# Create your models here.
class User(AbstractUser, PermissionsMixin):
    user_login = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=20)
    user_gender = models.BooleanField(default=False)
    user_postcode = models.IntegerField(default=False)
    user_phone_number = models.IntegerField(default=False)
    number_of_votes = models.IntegerField(default=0)
    current_trail = ForeignKey('Trail', on_delete=models.CASCADE, null=True)
    visited_trails = models.ManyToManyField('Trail', related_name='visited_by_users', blank=True)

    def end_hike(self):
        if self.current_trail is not None:
            self.visited_trails.add(self.current_trail)
            self.current_trail = None
            self.save()
        else:
            raise Exception("There is no current trail to end.")

    def get_visited_trails(self):
        return self.visited_trails.all()

    def get_current_trail(self):
        return self.current_trail


class Trail(models.Model):
    trail_id = models.IntegerField(primary_key=True),
    trail_title = models.TextField(max_length=40)
    trail_preview = models.TextField(max_length=1000)
    trail_short_description = models.TextField(max_length=100)
    trail_description = models.TextField(max_length=500)
    region = models.ForeignKey("Region", on_delete=models.CASCADE)


class CurrentState(models.Model):
    id = models.IntegerField(primary_key=True)
    basic_state = models.BooleanField(default=True)
    federal_state = models.BooleanField(default=False)


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=200)
    region_preview = models.TextField(max_length=500)
    short_description = models.TextField(max_length=500)
    big_region = models.ForeignKey("BigRegion", on_delete=models.CASCADE, null=True)
    count_of_votes = models.IntegerField(default=0)


class BigRegion(models.Model):
    big_region_id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=200)
    region_preview = models.TextField(max_length=500)
    short_description = models.TextField(max_length=500)
