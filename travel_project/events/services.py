import json
import re
from recommendations.ollama_utils import call_ollama
from .models import Event
from django.utils import timezone

def extract_json_blocks(text):
    """
    Extrage blocurile JSON dintre ```json și ``` din textul AI.
    Returnează o listă de dicționare Python.
    """
    pattern = r"```json\s*(\[\s*{.*?}\s*\])\s*```"
    matches = re.findall(pattern, text, flags=re.DOTALL)
    results = []
    for match in matches:
        try:
            data = json.loads(match)
            if isinstance(data, list):
                results.extend(data)
        except json.JSONDecodeError:
            continue
    return results

def generate_ai_events(location, user=None):
    """
    Generează evenimente AI pentru o locație, le curăță și le salvează doar pe cele valide.
    Returnează lista de evenimente create.
    """
    prompt = f"""
    Generează 3 evenimente turistice pentru locația {location.name}.
    Returnează STRICT JSON valid cu câmpurile:
    - title (string)
    - description (string)
    - category (string)
    - date (string, format YYYY-MM-DD)
    """

    response_text = call_ollama(prompt)
    events_data = extract_json_blocks(response_text)
    created_events = []

    for e in events_data:
        title = (e.get("title") or "").strip()
        description = (e.get("description") or "Fără descriere").strip()
        category = (e.get("category") or "General").strip()
        date_str = e.get("date") or e.get("date (în format YYYY-MM-DD)")

        # Skip dacă nu există titlu sau dată
        if not title or not date_str:
            continue

        # Verificare duplicate
        if Event.objects.filter(title=title, date=date_str, location=location, is_ai_generated=True).exists():
            continue

        # Creare eveniment valid
        try:
            event = Event.objects.create(
                location=location,
                title=title,
                description=description,
                category=category,
                date=date_str,
                created_by=user if user else None,
                is_ai_generated=True
            )
            created_events.append(event)
        except Exception as ex:
            print(f"Eroare la crearea evenimentului AI: {title}, {ex}")
            continue

    return created_events