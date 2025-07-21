from django import forms
from .models import Location

class LocationFilterForm(forms.Form):
    climate = forms.ChoiceField(
        required=False,
        choices=[('', 'Orice climă')] + [(c, c) for c in Location.objects.values_list('climate', flat=True).distinct() if c],
        label='Climă'
    )
    activities = forms.CharField(
        required=False,
        label='Activități conțin'
    )