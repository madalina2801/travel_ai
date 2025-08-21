import json
from recommendations.ollama_utils import call_ollama
from .models import Event
from django.utils.timezone import now,timedelta


def generate_ai_events(location, user=None):
    prompt = f"""
Generează o listă JSON cu 3 evenimente pentru {location.name}.
Format exact:
[
  {{
    "title": "...",
    "description": "...",
    "category": "...",
    "date (în format YYYY-MM-DD)": "..."
  }},
  ...
]
Returnează STRICT JSON valid, fără explicații.
"""
    response_text = call_ollama(prompt)  # asta e deja un string

    try:
        events_data = json.loads(response_text)  # încearcă să parsezi direct JSON
    except json.JSONDecodeError:
        # fallback: dacă nu vine JSON valid, îl spargem pe linii
        events_data = [{"title": line, "description": line, "category": "other"}
                       for line in response_text.split("\n") if line.strip()]

    from .models import Event
    generated_events = []
    for e in events_data:
        event = Event.objects.create(
            title=e.get("title", "Eveniment AI"),
            description=e.get("description", ""),
            category=e.get("category", "other"),
            location=location,
            created_by=user,
            is_ai_generated=True,
            date=now().date(),
        )
        generated_events.append(event)

    return generated_events