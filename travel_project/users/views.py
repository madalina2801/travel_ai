from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserProfileForm
from .models import UserProfile

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('recommendation_list')  # Or any page you prefer
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'users/edit_profile.html', {'form': form})

# Create your views here.
