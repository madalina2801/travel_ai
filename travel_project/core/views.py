from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, F, Q
from travel_project.events.models import Event
from travel_project.activities.models import Activity
from travel_project.locations.models import Location

def home_view(request):
    today = timezone.now().date()  # dacă Event.date e DateField
    
    activities = Activity.objects.all()[:6]

    upcoming_events = Event.objects.all()[:6]
    limited_events = Event.objects.annotate(
    participants_count=Count('participants'),
    available_slots=F('max_participants') - Count('participants')
).filter(
    date__gte=today,
    max_participants__isnull=False,
    available_slots__lte=5  # în loc de 2, ca să vezi mai multe
).order_by('date')[:6]

    context = {
        'activities': activities,
        'upcoming_events': upcoming_events,
        'limited_events': limited_events,
    }
    return render(request, 'home.html', context)

def search_view(request):
    query = request.GET.get('q', '')
    results_events = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )
    results_locations = Location.objects.filter(name__icontains=query)
    results_activities = Activity.objects.filter(name__icontains=query)
    
    context = {
        'query': query,
        'results_events': results_events,
        'results_locations': results_locations,
        'results_activities': results_activities,
    }
    return render(request, 'search_results.html', context)
