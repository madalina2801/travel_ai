from django.urls import path
from .views import location_list_view,location_detail_view,favorite_locations_view
from . import views

app_name = 'locations'  # << adaugă asta

urlpatterns = [
    path('', location_list_view, name='location_list'),
    path('<int:pk>/', location_detail_view, name='location_detail'),
    path('toggle_favorite/<int:location_id>/', views.toggle_favorite_location, name='toggle_favorite'),
    path('<int:location_id>/favorite/', views.toggle_favorite_location, name='toggle_favorite'),
]