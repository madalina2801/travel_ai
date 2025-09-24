from django.contrib import admin
from .models import Event, Location

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_ai_generated', 'location')
    list_filter = ('is_ai_generated', 'date')
    search_fields = ('title', 'description')
