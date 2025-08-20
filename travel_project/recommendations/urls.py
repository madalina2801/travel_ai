from django.urls import path
from .views import generate_recommendation, recommendation_list, recommendation_detail, delete_recommendation

urlpatterns = [
       path('generate/', generate_recommendation, name='generate_recommendation'),
       path('', recommendation_list, name='recommendation_list'),
       path('<int:pk>/', recommendation_detail, name='recommendation_detail'),
       path('delete/<int:pk>/', delete_recommendation, name='delete_recommendation'),
]