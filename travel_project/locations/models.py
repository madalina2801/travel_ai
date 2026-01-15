from django.db import models
from django.contrib.auth.models import User
from travel_project.activities.models import Activity

CLIMATE_CHOICES = [
    ('', 'Orice climă'),
    ('tropical', 'Tropical'),
    ('temperate', 'Temperat'),
    ('arid', 'Arid'),
    ('polar', 'Polar'),
    ('rece', 'Rece'),  
]

class Location(models.Model):
    name= models.CharField(max_length=255)
    description = models.TextField()
    climate = models.CharField(max_length=50, choices=CLIMATE_CHOICES)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #activities = models.ManyToManyField('activities.Activity', related_name='locations', blank=True)
       
    def __str__(self):
        return self.name
    
# Create your models here.
