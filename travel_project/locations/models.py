from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name= models.CharField(max_length=255)
    description = models.TextField()
    climate = models.CharField(max_length=100, blank=True, null=True)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activities = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.name
    
# Create your models here.
