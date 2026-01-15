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
from core.views import home_view,search_view
from django.shortcuts import redirect
from events.views import event_participate

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home & search
    path('', home_view, name='home'),
    path('search/', search_view, name='search'),

    # Core
    path('core/', include('core.urls')),

    # Recommendations
    path('recommendations/', include('recommendations.urls')),

    # Auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Users / profiles
    path('accounts/', include('users.urls')),
    path('profile/', include('users.urls')),

    # Itineraries
    path('itineraries/', include('itineraries.urls')),

    # Locations
    path('locations/', include('locations.urls')),

    # Activities
    path('activities/', include('activities.urls')),
    path('', lambda request: redirect('activities:activity_list')),

    # Events
    path('events/', include('events.urls')),
    path(
        'events/<int:pk>/participate/',
        event_participate,
        name='event_participate'
    ),
]
