"""
URL configuration for travel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from core.views import home_view
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('core/', include('core.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('users.urls')),
    path('profile/', include('users.urls')),
    path('itineraries/', include('itineraries.urls')), # Include itineraries app URLs
    path('locations/', include('locations.urls')),  # Include locations app URLs
    path('', lambda request: redirect('activities:activity_list')),
    path('activities/', include('activities.urls')),  # Include activities app URLs
]
