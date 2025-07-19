from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Recommendation
from users.models import UserProfile
from datetime import timedelta



@login_required
def generate_recommendation(request):
    user_profile = UserProfile.objects.get(user=request.user)

    # Creează o recomandare simplă, cu date exemplu bazate pe profil
    location = "București"  # poți adapta
    start_date = user_profile.travel_start or None
    end_date = user_profile.travel_end or (user_profile.travel_start + timedelta(days=7) if user_profile.travel_start else None)
    budget = user_profile.budget

    tags = user_profile.interests or "general"

    # Exemplu de text pentru cazare, obiective, restaurante
    accommodation = "Hotel Central, 3 stele"
    attractions = "Muzeul Național, Parcul Herăstrău"
    restaurants = "Caru' cu Bere, La Mama"

    # Creăm obiectul Recommendation în baza de date
    recommendation = Recommendation.objects.create(
        user_profile=user_profile,
        location=location,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        accommodation=accommodation,
        attractions=attractions,
        restaurants=restaurants,
        tags=tags
    )

    # Redirecționăm către lista recomandărilor, cu mesaj simplu
    return HttpResponseRedirect(reverse('recommendation_list'))

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
