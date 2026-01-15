from django import forms
from .models import Location
from activities.models import Activity

CLIMATE_CHOICES = [
    ('', 'Orice climă'),
    ('tropical', 'Tropical'),
    ('temperate', 'Temperat'),
    ('arid', 'Arid'),
    ('polar', 'Polar'),
    ('rece', 'Rece'),  
]

class LocationFilterForm(forms.Form):
    climate = forms.ChoiceField(
        choices=CLIMATE_CHOICES,
        required=False,
        label="Climă"
    )
    activities = forms.ModelChoiceField(
        queryset=Activity.objects.all(),
        required=False,
        empty_label="Orice activitate",
        label="Activitate"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        climates = Location.objects.values_list('climate', flat=True).distinct()
        self.fields['climate'].choices = [('', 'Orice climă')] + [(c, c) for c in climates if c]

        activities = Activity.objects.values_list('name', 'name').distinct()
        self.fields['activities'].queryset = Activity.objects.all()