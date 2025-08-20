from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from .models import UserProfile
from itineraries.models import Itinerary
from recommendations.views import generate_ai_recommendation
from recommendations.models import Recommendation

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('recommendation_list')  
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_locations = user_profile.favorite_locations.all()
    itineraries = Itinerary.objects.filter(user=user_profile)
    recommendations = Recommendation.objects.filter(user_profile=user_profile)
    
    return render(request, 'users/profile.html', {
        'user': request.user,
        'favorite_locations': favorite_locations,
        'itineraries': itineraries,
        'recommendations': recommendations,
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loghează automat după înregistrare
            return redirect('home')  # redirect către homepage sau profil
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})
# Create your views here.
