from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'club', 'nationality', 'get_age', 'created_at']
    list_filter = ['position', 'nationality', 'preferred_foot']
    search_fields = ['full_name', 'club', 'nationality']