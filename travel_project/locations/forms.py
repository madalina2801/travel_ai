from django import forms
from .models import Location
from activities.models import Activity

class LocationFilterForm(forms.Form):
    climate = forms.ChoiceField(required=False, choices=[], label='Climă')
    activities = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        required=False,
        empty_label="Toate activitățile"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        climates = Location.objects.values_list('climate', flat=True).distinct()
        self.fields['climate'].choices = [('', 'Orice climă')] + [(c, c) for c in climates if c]

        activities = Activity.objects.values_list('name', 'name').distinct()
        self.fields['activities'].choices = [('', 'Orice activitate')] + list(activities)