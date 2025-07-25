from django.contrib import admin
from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate', 'interest_type', 'get_location')
    list_filter = ('climate', 'interest_type')
    search_fields = ('name', 'description')
# Register your models here.
