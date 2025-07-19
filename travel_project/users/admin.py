from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferences', 'budget', 'favorite_activities')
    search_fields = ('user__username', 'preferences', 'favorite_activities')
    list_filter = ('user',)

# Register your models here.
