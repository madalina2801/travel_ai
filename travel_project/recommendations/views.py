from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import RecommendationRequestForm
from .models import Recommendation
from users.models import UserProfile
import openai

openai.api_key = ""

@login_required
def generate_recommendation(request):
    if request.method == 'POST':
        form = RecommendationRequestForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            user_profile = UserProfile.objects.get(user=request.user)

            response = openai.ChatCompletion.create(
                   model="gpt-3.5-turbo",  # sau "gpt-4" dacă ai acces
                   messages=[
                          {"role": "system", "content": "You are a helpful travel assistant."},
                          {"role": "user", "content": prompt}
                          ],
                          max_tokens=150
                          )
            text = response['choices'][0]['message']['content'].strip()

            Recommendation.objects.create(
                user_profile=user_profile,
                prompt=prompt,
                text=text
            )

            return redirect('recommendation_list')
        else:
            print("Formular invalid:", form.errors)
    else:
        form = RecommendationRequestForm()

    return render(request, 'recommendations/generate.html', {'form': form})

@login_required
def recommendation_list(request):
    user_profile = UserProfile.objects.get(user=request.user)
    recommendations = Recommendation.objects.filter(user_profile__user=request.user)
    return render(request, 'recommendations/list.html', {'recommendations': recommendations})

# Create your views here.
