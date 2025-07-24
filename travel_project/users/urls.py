from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
]