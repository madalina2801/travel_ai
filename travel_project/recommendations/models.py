from django.db import models
from django.conf import settings
from locations.models import Location
from users.models import UserProfile


class Recommendation(models.Model):
       STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
       user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
       location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
       start_date = models.DateField()
       end_date = models.DateField()
       budget = models.DecimalField(max_digits=10, decimal_places=2)
       
       accommodation = models.TextField(blank=True)
       attractions = models.TextField(blank=True)
       restaurants = models.TextField(blank=True)
       tags = models.CharField(max_length=255, help_text="Taguri separate prin virgulă. Ex: plajă, istorie, natură", db_index=True, blank=True)
       
       created_at = models.DateTimeField(auto_now_add=True)
       status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
       
       def __str__(self):
           return f"Recomandare pentru {self.user_profile.user.username} în {self.location}"
# Create your models here.
