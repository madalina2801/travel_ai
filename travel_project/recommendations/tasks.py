from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def generate_recommendation_task(self, recommendation_id: int):
    """
    Celery task — picked up from RabbitMQ by the worker.

    Flow:
      1. Load the pending Recommendation by ID.
      2. Call Ollama (the existing logic, untouched).
      3. Populate the recommendation fields and mark it complete.
      4. On any failure, retry up to 3 times then mark as failed.
    """
    from .models import Recommendation
    from users.models import UserProfile
    from locations.models import Location
    from .ollama_utils import call_ollama
    import random

    try:
        recommendation = Recommendation.objects.get(pk=recommendation_id)
        user_profile = recommendation.user_profile

        logger.info(
            "Worker picked up recommendation task",
            extra={"recommendation_id": recommendation_id, "user": user_profile.user.username}
        )

        # ── Build the prompt (identical to original logic) ─────────────────
        accommodation_pref = user_profile.accommodation_preference or "nu a specificat"
        restaurant_pref    = user_profile.restaurant_preference    or "nu a specificat"

        previous_locations = (
            Recommendation.objects
            .filter(user_profile=user_profile, status="completed")
            .exclude(pk=recommendation_id)
            .values_list('location__name', flat=True)
        )
        exclude_cities = ', '.join(previous_locations) if previous_locations else "Nicio locație anterioară"
        random_seed = random.randint(1000, 9999)

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

        # ── Call Ollama ─────────────────────────────────────────────────────
        ai_response = call_ollama(prompt).strip()
        lines = [
            line.strip()
            for line in ai_response.split('\n')
            if line.strip().startswith(tuple("12345"))
        ]

        if len(lines) < 5:
            raise ValueError(f"Răspunsul AI nu conține toate cele 5 secțiuni: {ai_response}")

        location_name = lines[0].replace("1. Locație:", "").strip()
        accommodation  = lines[1].replace("2. Cazare:", "").strip()
        attractions    = lines[2].replace("3. Atracții:", "").strip()
        restaurants    = lines[3].replace("4. Restaurante:", "").strip()
        tags           = lines[4].replace("5. Taguri:", "").strip()

        # ── Persist location ────────────────────────────────────────────────
        location, _ = Location.objects.get_or_create(
            name=location_name,
            defaults={"description": "Descriere generată AI"},
        )

        # ── Update the recommendation record ───────────────────────────────
        recommendation.location    = location
        recommendation.start_date  = user_profile.travel_start
        recommendation.end_date    = user_profile.travel_end
        recommendation.budget      = user_profile.budget
        recommendation.accommodation = accommodation
        recommendation.attractions   = attractions
        recommendation.restaurants   = restaurants
        recommendation.tags          = tags
        recommendation.status        = "completed"
        recommendation.save()

        logger.info("Recommendation completed", extra={"recommendation_id": recommendation_id})

    except Recommendation.DoesNotExist:
        # Don't retry — the record is gone
        logger.error("Recommendation not found", extra={"recommendation_id": recommendation_id})

    except Exception as exc:
        logger.warning(
            "Recommendation task failed, retrying",
            extra={"recommendation_id": recommendation_id, "error": str(exc)}
        )
        # Retry: Celery re-queues the task message back into RabbitMQ
        raise self.retry(exc=exc)
