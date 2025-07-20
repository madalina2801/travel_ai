from django import forms
from .models import Itinerary
from locations.models import Location

class ItineraryForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    days = forms.IntegerField(min_value=1, label="Număr de zile")

    class Meta:
        model = Itinerary
        fields = ['location', 'days']