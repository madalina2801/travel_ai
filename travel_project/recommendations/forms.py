from django import forms

class RecommendationRequestForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Scrie ce fel de recomandare vrei"
    )