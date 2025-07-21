from django.urls import path
from .views import generate_itinerary_view, itinerary_detail_view,itinerary_list_view

urlpatterns = [
    path('', itinerary_list_view, name='itinerary_list'),
    path('itineraries/generate', generate_itinerary_view, name='generate_itinerary'),
    path('<int:itinerary_id>/', itinerary_detail_view, name='itinerary_detail'),
]