from django.urls import path
from . import views

urlpatterns = [
       path('generate/', views.generate_recommendation, name='generate_recommendation'),
       path('list/', views.recommendation_list, name='recommendation_list'),
]