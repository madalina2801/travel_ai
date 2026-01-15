from django.contrib.auth.models import User
from django.db import models
from locations.models import Location


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Preferințe personale
    budget = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    preferred_season = models.CharField(max_length=20, choices=[
        ('spring', 'Primăvară'),
        ('summer', 'Vara'),
        ('autumn', 'Toamnă'),
        ('winter', 'Iarna'),
        ('any', 'Oricare'),
    ], default='any')

    preferred_climate = models.CharField(max_length=50, choices=[
        ('tropical', 'Tropical'),
        ('temperate', 'Temperate'),
        ('arctic', 'Arctic'),
    ], null=True, blank=True)
    
    # Interese de călătorie
    interests = models.TextField(help_text="Interese separate prin virgulă. Ex: plajă, munte, cultură")

    # Perioada de vacanță preferată
    travel_start = models.DateField(null=True, blank=True)
    travel_end = models.DateField(null=True, blank=True)

    accommodation_preference = models.CharField(max_length=255, null=True, blank=True)
    restaurant_preference = models.CharField(max_length=255, null=True, blank=True)
    preferred_activities = models.CharField(max_length=100, null=True, blank=True)  # opțional
    favorite_locations = models.ManyToManyField(Location, blank=True, related_name='favorited_by')

    def __str__(self):
        return f"Profilul utilizatorului {self.user.username}"