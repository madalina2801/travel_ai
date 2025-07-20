from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate', 'average_cost')
    search_fields = ('name', 'climate')
# Register your models here.
