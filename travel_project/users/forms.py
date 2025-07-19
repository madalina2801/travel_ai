from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'budget', 'preferred_season', 'interests', 
            'travel_start', 'travel_end',
            'accommodation_preference', 'restaurant_preference'
        ]
        widgets = {
            'travel_start': forms.DateInput(attrs={'type': 'date'}),
            'travel_end': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'interests': 'Interese separate prin virgulă.<br>Ex: plajă, munte, cultură',
            # poți adăuga și pentru altele dacă vrei
        }