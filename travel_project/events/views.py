from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm, CommentForm
from django.db.models import Count, F
from django.db.models.functions import Coalesce
# Create your views here.
def event_list(request):

    # Evenimente AI
    events_ai = Event.objects.filter(is_ai_generated=True).annotate(
        participants_count=Coalesce(Count('participants'), 0),
        max_participants_filled=Coalesce('max_participants', 0)
    ).annotate(
        available_slots=F('max_participants_filled') - F('participants_count')
    ).order_by("date")

    # Evenimente comunitate
    events_user = Event.objects.filter(is_ai_generated=False).annotate(
        participants_count=Coalesce(Count('participants'), 0),
        max_participants_filled=Coalesce('max_participants', 0)
    ).annotate(
        available_slots=F('max_participants_filled') - F('participants_count')
    ).order_by("date")

    context = {
        "events_ai": events_ai,
        "events_user": events_user,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        
        form= CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = CommentForm()

    return render(request, 'events/event_detail.html', {'event': event, 'comments': comments, 'form': form})

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
    else:
        event.participants.add(request.user)
    return redirect('event_detail', pk=event.pk)

@login_required
def event_participate(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user

    if user.is_authenticated:
        # verificăm dacă există limită și dacă mai sunt locuri
        if event.max_participants is None or event.participants.count() < event.max_participants:
            event.participants.add(user)
            event.save()

    return redirect('event_list')