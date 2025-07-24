from django.db import models


CLIMATE_CHOICES = [
    ('tropical', 'Tropical'),
    ('temperate', 'Temperate'),
    ('arid', 'Arid'),
    ('polar', 'Polar'),
]

INTEREST_CHOICES = [
    ('adventure', 'Adventure'),
    ('cultural', 'Cultural'),
    ('relaxation', 'Relaxation'),
    ('nature', 'Nature'),
]

class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    climate = models.CharField(max_length=50, choices=CLIMATE_CHOICES)
    interest_type = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_locations(self):
        return ", ".join([loc.name for loc in self.locations.all()])
    get_locations.short_description = 'Locations'

# Create your models here.
