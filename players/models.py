from django.db import models
from django.contrib.auth.models import User

POSITION_CHOICES = [
    ('GK', 'Goalkeeper'),
    ('CB', 'Centre Back'),
    ('LB', 'Left Back'),
    ('RB', 'Right Back'),
    ('CDM', 'Defensive Midfielder'),
    ('CM', 'Central Midfielder'),
    ('CAM', 'Attacking Midfielder'),
    ('LW', 'Left Winger'),
    ('RW', 'Right Winger'),
    ('ST', 'Striker'),
    ('CF', 'Centre Forward'),
]

FOOT_CHOICES = [
    ('Left', 'Left'),
    ('Right', 'Right'),
    ('Both', 'Both'),
]

class Player(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    club = models.CharField(max_length=255)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    preferred_foot = models.CharField(max_length=20, choices=FOOT_CHOICES)
    height = models.IntegerField(help_text="სიმაღლე სმ-ში")
    weight = models.IntegerField(help_text="წონა კგ-ში")
    market_value = models.IntegerField(null=True, blank=True, help_text="ევროში")
    contract_expiry = models.DateField(null=True, blank=True)
    agent = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='players/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('CB', 'Centre Back'),
        ('LB', 'Left Back'),
        ('RB', 'Right Back'),
        ('CDM', 'Defensive Midfielder'),
        ('CM', 'Central Midfielder'),
        ('CAM', 'Attacking Midfielder'),
        ('LW', 'Left Winger'),
        ('LM', 'Left Midfielder'),
        ('RW', 'Right Winger'),
        ('RM', 'Right Midfielder'),
        ('ST', 'Striker'),
        ('CF', 'Centre Forward'),
    ]
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_players')

    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    def get_age(self):
        from datetime import date
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_average_rating(self):
        reports = self.report_set.all()
        if reports:
            return round(sum(r.rating for r in reports) / len(reports), 1)
        return None
    
class Shortlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'player']

    def __str__(self):
        return f"{self.user.username} → {self.player.full_name}"