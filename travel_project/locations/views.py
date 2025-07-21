from django.shortcuts import render, redirect, get_object_or_404
from .models import Location
from .forms import LocationFilterForm
from users.models import UserProfile
from recommendations.ollama_utils import call_ollama
from django.contrib.auth.decorators import login_required

def location_list_view(request): 
    locations = Location.objects.all()
    form = LocationFilterForm(request.GET or None)

    if form.is_valid():
        climate = form.cleaned_data.get('climate')
        activities = form.cleaned_data.get('activities')

        if climate:
            locations = locations.filter(climate__icontains=climate)
        if activities:
            locations = locations.filter(activities__icontains=activities)

    # Obținem preferințele din profilul utilizatorului (dacă există)
    preferences = ''
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            preferences = f"{user_profile.preferred_climate or ''}, {user_profile.preferred_activities or ''}"
        except UserProfile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None

    # Pregătim datele pentru AI
    locations_data = [
        {'id': l.id, 'name': l.name, 'climate': l.climate, 'activities': l.activities}
        for l in locations
    ]
    prompt = (
        f"Clasifică următoarele locații după relevanța lor pentru un utilizator care preferă: {preferences}. "
        f"Returnează doar o listă JSON cu ID-urile în ordinea descrescătoare a recomandării. Ex: [3, 1, 5]\n"
        f"Locații disponibile: {locations_data}"
    )

    try:
        ranked_ids = eval(call_ollama(prompt))
        id_to_location = {loc.id: loc for loc in locations}
        sorted_locations = [id_to_location[i] for i in ranked_ids if i in id_to_location]
    except Exception:
        sorted_locations = locations  # fallback dacă AI-ul eșuează

    # Obținem ID-urile locațiilor favorite ale utilizatorului
    favorite_location_ids = set()
    if request.user.is_authenticated and user_profile:
        favorite_location_ids = set(user_profile.favorite_locations.values_list('id', flat=True))

    return render(request, 'locations/location_list.html', {
        'form': form,
        'locations': sorted_locations,
        'favorite_location_ids': favorite_location_ids
    })


def location_detail_view(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'locations/location_detail.html', {'location': location})


@login_required
def toggle_favorite_location(request, location_id):
    user_profile = UserProfile.objects.get(user=request.user)
    location = get_object_or_404(Location, id=location_id)

    if location in user_profile.favorite_locations.all():
        user_profile.favorite_locations.remove(location)
    else:
        user_profile.favorite_locations.add(location)
    
    return redirect('locations:location_list')  # redirecționează către lista locațiilor

@login_required
def favorite_locations_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorites = user_profile.favorite_locations.all()
    return render(request, 'locations/favorite_locations.html', {
        'favorites': favorites
    })
# Create your views here.