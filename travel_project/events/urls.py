from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("add/", views.add_event, name="add_event"),
    path("<int:pk>/join/", views.join_event, name="join_event"),
    path('events/<int:pk>/participate/', views.event_participate, name='event_participate'),
]