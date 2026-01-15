from datetime import date
from django.db import models
from django.contrib.auth.models import User
from travel_project.locations.models import Location
# Create your models here.

class Event(models.Model):
    CATEGORY_CHOICES = [
        ("festival", "Festival"),
        ("concert", "Concert"),
        ("market", "Market"),
        ("sports","Eveniment sportiv"),
        ("exhibition", "Expozitie"),
        ("other", "Other"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='events')
    category= models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_ai_generated = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='event_participants', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_participants = models.PositiveIntegerField(default=0) 
     
    def save(self, *args, **kwargs):
        if not self.date:
            self.date = date.today()  # sau altă dată default
        super().save(*args, **kwargs)

    def __str__(self):
        if self.date:
            return f"{self.title} - {self.location.name} on {self.date.strftime('%Y-%m-%d')}"
        return f"{self.title} - {self.location.name}"
    
class Comment(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentariu de la  {self.user.username} la {self.event.title}" 