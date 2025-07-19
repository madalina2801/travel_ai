from django.urls import path
from . import views

urlpatterns = [
       path('', views.recommendation_list, name='recommendation_list'),
       path('generate/', views.generate_recommendation, name='generate_recommendation'),
]