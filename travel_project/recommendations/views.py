from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from users.models import UserProfile
from datetime import timedelta
from locations.models import Location
from .ollama_utils import call_ollama




def generate_ai_recommendation(user_profile):
    # Evită duplicate pentru același user și interval
    existing = Recommendation.objects.filter(
        user_profile=user_profile,
        start_date=user_profile.travel_start,
        end_date=user_profile.travel_end,
    ).first()
    if existing:
        return existing

    # Preferințele fallback
    accommodation_pref = user_profile.accommodation_preference or "nu a specificat"
    restaurant_pref = user_profile.restaurant_preference or "nu a specificat"

    # Prompt îmbunătățit
    prompt = f"""
Creează o recomandare turistică personalizată pentru un utilizator cu:
- Buget: {user_profile.budget} EUR
- Perioada: {user_profile.travel_start} până la {user_profile.travel_end}
- Interese: {user_profile.interests}
- Preferințe cazare: {accommodation_pref}
- Preferințe restaurante: {restaurant_pref}

Returnează doar următoarele 5 linii (una per secțiune), fără introduceri sau explicații:

1. Locație: <oraș, țară>
2. Cazare: <hoteluri, prețuri, tipuri>
3. Atracții: <obiective turistice și activități>
4. Restaurante: <restaurante și specific culinar>
5. Taguri: <etichete separate prin virgulă>
"""

    ai_response = call_ollama(prompt).strip()
    
    # Extrage doar cele 5 linii numerotate
    lines = [line.strip() for line in ai_response.split('\n') if line.strip().startswith(tuple("12345"))]

    if len(lines) < 5:
        raise ValueError(f"Răspunsul AI nu conține toate cele 5 secțiuni: {ai_response}")

    # Curăță fiecare linie
    location_name = lines[0].replace("1. Locație:", "").strip()
    accommodation = lines[1].replace("2. Cazare:", "").strip()
    attractions = lines[2].replace("3. Atracții:", "").strip()
    restaurants = lines[3].replace("4. Restaurante:", "").strip()
    tags = lines[4].replace("5. Taguri:", "").strip()

    # Caută sau creează locația
    location = Location.objects.filter(name=location_name).first()
    if not location:
        location = Location.objects.create(name=location_name, description="Descriere generată AI")

    # Creează recomandarea
    return Recommendation.objects.create(
        user_profile=user_profile,
        location=location,
        start_date=user_profile.travel_start,
        end_date=user_profile.travel_end,
        budget=user_profile.budget,
        accommodation=accommodation,
        attractions=attractions,
        restaurants=restaurants,
        tags=tags,
    )

@login_required
def generate_recommendation(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        generate_ai_recommendation(user_profile)
        return redirect('recommendation_list')

    except Exception as e:
        return render(request, "recommendations/error.html", {
            "message": f"Eroare generare AI: {str(e)}"
        })



@login_required
def recommendation_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, "recommendations/missing_data.html", {
            "message": "Nu ai un profil complet. Te rugăm să îți creezi unul."
        })

    # Check required fields are present
    if not user_profile.budget or not user_profile.travel_start or not user_profile.travel_end:
        return render(request, "recommendations/missing_data.html", {
            "message": "Te rugăm să îți completezi profilul (buget, perioadă) pentru a primi recomandări."
        })

    recommendations = Recommendation.objects.filter(
        budget__lte=user_profile.budget,
        start_date__gte=user_profile.travel_start,
        end_date__lte=user_profile.travel_end,
    )

    return render(request, "recommendations/list.html", {
        "recommendations": recommendations
    })
# Create your views here.
