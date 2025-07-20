from django.shortcuts import render
from .models import Location


def location_list_view(request):
    locations = Location.objects.all()
    return render(request, 'locations/location_list.html', {'locations': locations})

# Create your views here.