from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.recommendation_list,       name='recommendation_list'),
    path('generate/',                 views.generate_recommendation,   name='generate_recommendation'),
    path('<int:pk>/',                 views.recommendation_detail,     name='recommendation_detail'),
    path('<int:pk>/delete/',          views.delete_recommendation,     name='delete_recommendation'),
    path('<int:pk>/processing/',      views.recommendation_processing, name='recommendation_processing'),
]