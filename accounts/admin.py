from django.contrib import admin
from django.contrib import messages
from .models import InviteCode

@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_used', 'used_by', 'created_at']
    list_filter = ['is_used']
    readonly_fields = ['is_used', 'used_by', 'created_by', 'created_at']

    def has_add_permission(self, request):
        return True  # ხელით დამატება დაბლოკილია

    def has_delete_permission(self, request, obj=None):
        return True  # წაშლაც დაბლოკილია