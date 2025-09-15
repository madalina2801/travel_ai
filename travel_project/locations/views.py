from django.shortcuts import render, redirect, get_object_or_404
from locations.models import Location
from activities.models import Activity
from .forms import LocationFilterForm
from users.models import UserProfile
from recommendations.ollama_utils import call_ollama
from django.contrib.auth.decorators import login_required
from events.services import generate_ai_events

def location_list_view(request): 
    locations = Location.objects.all()
    form = LocationFilterForm(request.GET or None)

    if form.is_valid():
        climate = form.cleaned_data.get('climate')
        activity_name = form.cleaned_data.get('activities')

        if climate:
            locations = locations.filter(climate__iexact=climate)
        if activity_name:
            locations = locations.filter(activity_set__name__iexact=activity_name)

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
    locations_data = []
    for loc in locations:
        activity_names = [a.name for a in loc.activity_set.all()]  # folosind related_name din ForeignKey
        locations_data.append({
        'id': loc.id,
        'name': loc.name,
        'climate': loc.climate,
        'activities': ', '.join(activity_names)
    })
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
    # dacă nu există evenimente generate, cerem AI-ului să creeze
    if not location.events.filter(is_ai_generated=True).exists():
        generate_ai_events(location, request.user if request.user.is_authenticated else None)

    events = location.events.all().order_by("date")
    
    return render(request, "locations/location_detail.html", {
        "location": location,
        "events": events
    })


@login_required
def toggle_favorite_location(request, location_id):
    user_profile = UserProfile.objects.get(user=request.user)
    location = get_object_or_404(Location, id=location_id)

    if location in user_profile.favorite_locations.all():
        user_profile.favorite_locations.remove(location)
    else:
        user_profile.favorite_locations.add(location)
    
    return redirect('locations:locations_list')  # redirecționează către lista locațiilor

@login_required
def favorite_locations_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorites = user_profile.favorite_locations.all()
    return render(request, 'locations/favorite_locations.html', {
        'favorites': favorites
    })
# Create your views here.