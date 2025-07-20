from django.urls import path
from .views import location_list_view

urlpatterns = [
    path('', location_list_view, name='location_list'),
]