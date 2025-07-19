from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferences = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    favorite_activities = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
# Create your models here.
