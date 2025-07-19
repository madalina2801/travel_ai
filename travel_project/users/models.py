from django.contrib.auth.models import User
from django.db import models


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
    
    # Interese de călătorie
    interests = models.TextField(help_text="Interese separate prin virgulă. Ex: plajă, munte, cultură")

    # Perioada de vacanță preferată
    travel_start = models.DateField(null=True, blank=True)
    travel_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profilul utilizatorului {self.user.username}"