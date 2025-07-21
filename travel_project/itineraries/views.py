from django.shortcuts import render,redirect
from .forms import ItineraryForm
from .models import Itinerary
from users.models import UserProfile
from recommendations.ollama_utils import call_ollama
from django.shortcuts import get_object_or_404
from locations.models import Location
import json
import re


def generate_itinerary_view(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            days = form.cleaned_data['days']
            user_profile = UserProfile.objects.get(user=request.user)

            prompt = (
                f"Generează un itinerar turistic în LIMBA ROMÂNĂ pentru {days} zile în {location.name}, "
                f"cu activități pe fiecare zi și un cost estimat total. "
                f"Returnează STRICT doar în format JSON, fără introduceri, explicații sau text adițional:\n"
                f'{{"location": "...", "days": ..., "schedule": {{"day 1": "...", "day 2": "..."}}, "estimated_cost": "..."}}'
            )

            try:
                response_raw = call_ollama(prompt).strip()

                # DEBUG
                print(">>> Prompt trimis:\n", prompt)
                print(">>> Răspuns AI brut:\n", response_raw)

                # Scoate backticks și eventualul "json" de la început și ``` de la sfârșit
                cleaned = re.sub(r"^```json\s*|\s*```$", "", response_raw.strip())

                print(">>> Răspuns AI curățat:\n", cleaned)

                response_json = json.loads(cleaned)

                plan_markdown = f"### Itinerar pentru {response_json['location']} ({response_json['days']} zile)\n\n"
                for zi, activitati in response_json["schedule"].items():
                    plan_markdown += f"**{zi.title()}**:\n{activitati}\n\n"
                plan_markdown += f"**Cost estimat:** {response_json['estimated_cost']}"

                estimated_cost = float(''.join(filter(lambda x: x.isdigit() or x == '.', response_json["estimated_cost"])))

            except json.JSONDecodeError as e:
                return render(request, 'itineraries/generate_itinerary.html', {
                    'form': form,
                    'error': f"Eroare AI: răspuns JSON invalid: {e}\nConținut:\n{cleaned}"
                })
            except Exception as e:
                return render(request, 'itineraries/generate_itinerary.html', {
                    'form': form,
                    'error': f"Eroare AI: {e}"
                })

            itinerary = Itinerary.objects.create(
                user=user_profile,
                location=location,
                days=days,
                plan_text=plan_markdown,
                estimated_cost=estimated_cost
            )

            return redirect('itinerary_detail', itinerary.id)

    else:
        initial = {}
        location_id = request.GET.get('location')
        if location_id:
            try:
                location = Location.objects.get(pk=location_id)
                initial['location'] = location
            except Location.DoesNotExist:
                pass
        form = ItineraryForm(initial=initial)

    return render(request, 'itineraries/generate_itinerary.html', {'form': form})


def itinerary_detail_view(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    return render(request, 'itineraries/itinerary_detail.html', {'itinerary': itinerary})

def itinerary_list_view(request):
    itineraries = Itinerary.objects.filter(user__user=request.user)
    return render(request, 'itineraries/itinerary_list.html', {
        'itineraries': itineraries
    })
# Create your views here.
