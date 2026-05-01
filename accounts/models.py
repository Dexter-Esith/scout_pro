from django.db import models
from django.contrib.auth.models import User
import random
import string

class InviteCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_codes')
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_code')
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} — {'Used' if self.is_used else 'Active'}"

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    @staticmethod
    def ensure_active_code(admin_user):
        """ყოველთვის ერთი აქტიური კოდი უნდა იყოს"""
        if not InviteCode.objects.filter(is_used=False).exists():
            InviteCode.objects.create(
                code=InviteCode.generate_code(),
                created_by=admin_user
            )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"