from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['budget', 'preferred_season', 'interests', 'travel_start', 'travel_end']
        widgets = {
            'travel_start': forms.DateInput(attrs={'type': 'date'}),
            'travel_end': forms.DateInput(attrs={'type': 'date'}),
        }