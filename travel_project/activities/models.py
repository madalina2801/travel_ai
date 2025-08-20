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
    location = models.ForeignKey(
        'locations.Location',
        on_delete=models.CASCADE,
        related_name='activity_set' 
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    climate = models.CharField(max_length=50, choices=CLIMATE_CHOICES)
    interest_type = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_location(self):
        return self.location.name if self.location else "-"
    get_location.short_description = 'Location'

# Create your models here.
