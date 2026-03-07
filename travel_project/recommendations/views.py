from sqlite3 import Connection

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Recommendation
from .tasks import generate_recommendation_task
from users.models import UserProfile
from kombu import Connection


# ── ASYNC entry point ────────────────────────────────────────────────────────
@login_required
def generate_recommendation(request):
    """
    Creates a pending Recommendation row immediately,
    then publishes a task to RabbitMQ via Celery.
    Returns to a 'processing' page — no blocking on Ollama.
    """
    try:
        user_profile = UserProfile.objects.get(user=request.user)

        if not user_profile.travel_start or not user_profile.travel_end:
            return render(request, "recommendations/missing_data.html", {
                "message": "Te rugăm să îți completezi perioada de călătorie în profil."
            })

        if not user_profile.budget:
            return render(request, "recommendations/missing_data.html", {
                "message": "Te rugăm să îți completezi bugetul în profil."
            })

        # 1. Create a placeholder record — worker will fill in the fields
        recommendation = Recommendation.objects.create(
            user_profile=user_profile,
            start_date=user_profile.travel_start,
            end_date=user_profile.travel_end,
            budget=user_profile.budget,
            status="pending",          # new field — see migration note below
        )

        # 2. Publish task message to RabbitMQ (non-blocking)
        with Connection('amqp://guest:guest@rabbitmq:5672//') as conn:
            with conn.channel():
                generate_recommendation_task.apply_async(
                    args=[recommendation.pk],
                    queue='recommendations',
                    connection=conn
                    )
        # 3. Redirect to a lightweight polling/status page
        return redirect('recommendation_processing', pk=recommendation.pk)

    except UserProfile.DoesNotExist:
        return render(request, "recommendations/missing_data.html", {
            "message": "Nu ai un profil complet. Te rugăm să îți creezi unul."
        })
    except Exception as e:
        return render(request, "recommendations/error.html", {
            "message": f"Eroare la trimiterea cererii: {str(e)}"
        })


# ── Polling status view ──────────────────────────────────────────────────────
@login_required
def recommendation_processing(request, pk):
    """
    Shows a 'your recommendation is being generated' page.
    Auto-refreshes every 3s; redirects to detail once status == 'completed'.
    """
    recommendation = get_object_or_404(Recommendation, pk=pk, user_profile__user=request.user)

    if recommendation.status == "completed":
        return redirect('recommendation_detail', pk=pk)

    if recommendation.status == "failed":
        return render(request, "recommendations/error.html", {
            "message": "Generarea recomandării a eșuat. Te rugăm să încerci din nou."
        })

    return render(request, "recommendations/processing.html", {
        "recommendation": recommendation
    })


# ── Unchanged views below ────────────────────────────────────────────────────

@login_required
def recommendation_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, "recommendations/missing_data.html", {
            "message": "Nu ai un profil complet. Te rugăm să îți creezi unul."
        })

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
        status="completed",            # only show finished recommendations
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
