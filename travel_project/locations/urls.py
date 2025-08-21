from django.urls import path
from .views import location_list_view,location_detail_view,favorite_locations_view
from . import views

app_name = 'locations'  

urlpatterns = [
    path('', views.location_list_view, name='locations_list'),
    path('<int:pk>/', location_detail_view, name='location_detail'),
     path('favorites/', favorite_locations_view, name='favorite_locations'),
    path('<int:location_id>/favorite/', views.toggle_favorite_location, name='toggle_favorite'),
]