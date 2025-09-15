from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm, CommentForm
# Create your views here.
def event_list(request):
    now = timezone.now()
    events_ai = Event.objects.filter(is_ai_generated=True).order_by("date")
    events_user = Event.objects.filter(is_ai_generated=False).order_by("date")

    print("NOW:", now)
    print("AI events:", list(events_ai.values("title", "date")))
    print("User events:", list(events_user.values("title", "date")))
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