from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from users.models import UserProfile
from datetime import timedelta
from locations.models import Location
from .ollama_utils import call_ollama
from django.contrib import messages
import random


def generate_ai_recommendation(user_profile):

    
    accommodation_pref = user_profile.accommodation_preference or "nu a specificat"
    restaurant_pref = user_profile.restaurant_preference or "nu a specificat"


    
    previous_locations = Recommendation.objects.filter(user_profile=user_profile).values_list('location__name', flat=True)
    exclude_cities = ', '.join(previous_locations) if previous_locations else "Nicio locație anterioară"

    
    random_seed = random.randint(1000, 9999)

    # Prompt pentru modelul AI
    prompt = f"""
Creează o recomandare turistică personalizată pentru un utilizator cu:
- Buget: {user_profile.budget} EUR
- Perioada: {user_profile.travel_start} până la {user_profile.travel_end}
- Interese: {user_profile.interests}
- Preferințe cazare: {accommodation_pref}
- Preferințe restaurante: {restaurant_pref}

Locații deja sugerate: {exclude_cities}
Seed aleator: {random_seed}

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
        if not user_profile.travel_start or not user_profile.travel_end:
            return render(request, "recommendations/missing_data.html", {
                "message": "Te rugăm să îți completezi perioada de călătorie în profil pentru a genera recomandări."
        })

        recommendation = generate_ai_recommendation(user_profile)
        return redirect('recommendation_detail', pk=recommendation.pk)

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
    location__isnull=False,
    location__id__isnull=False,
    budget__lte=user_profile.budget,
    start_date__gte=user_profile.travel_start,
    end_date__lte=user_profile.travel_end,
)

    return render(request, "recommendations/list.html", {
        "recommendations": recommendations
    })

@login_required
def delete_recommendation(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk, user_profile__user=request.user)
    recommendation.delete()
    messages.success(request, "Recomandarea a fost ștearsă.")
    return redirect('recommendation_list')

@login_required
def recommendation_detail(request, pk):
    recommendation = get_object_or_404(Recommendation, pk=pk, user_profile__user=request.user)
    return render(request, 'recommendations/detail.html', {
        'recommendation': recommendation
    })

# Create your views here.
