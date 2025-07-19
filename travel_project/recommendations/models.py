from django.db import models
from django.conf import settings
from locations.models import Location
from users.models import UserProfile


class Recommendation(models.Model):
       user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
       location = models.CharField(max_length=100)
       start_date = models.DateField()
       end_date = models.DateField()
       budget = models.DecimalField(max_digits=10, decimal_places=2)
       
       accommodation = models.TextField()
       attractions = models.TextField()
       restaurants = models.TextField()
       
       tags = models.CharField(max_length=255, help_text="Taguri separate prin virgulă. Ex: plajă, istorie, natură")
       
       created_at = models.DateTimeField(auto_now_add=True)
       
       def __str__(self):
           return f"Recomandare pentru {self.user_profile.user.username} în {self.location}"
# Create your models here.
