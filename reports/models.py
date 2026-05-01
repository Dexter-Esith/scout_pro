from django.db import models
from django.contrib.auth.models import User
from players.models import Player

class Report(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    scout = models.ForeignKey(User, on_delete=models.CASCADE)
    match_name = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    strengths = models.TextField()
    weaknesses = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.player.full_name} - {self.match_name} ({self.rating})"