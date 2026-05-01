from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['player', 'scout', 'match_name', 'rating', 'created_at']
    list_filter = ['rating', 'scout']
    search_fields = ['player__full_name', 'match_name']