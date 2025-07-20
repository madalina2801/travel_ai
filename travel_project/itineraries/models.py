from django.db import models
from users.models import UserProfile
from locations.models import Location

class Itinerary(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    days = models.PositiveIntegerField()
    plan_text = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Itinerar pentru  {self.user_profile.username} in {self.location.name} ({self.days} zile)"

# Create your models here.
