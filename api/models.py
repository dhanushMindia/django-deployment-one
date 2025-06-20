# api/models.py
from django.db import models

class Competition(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    TEAM_CHOICES = [
        ('Individual', 'Individual'),
        ('Team', 'Team'),
        ('Both', 'Both'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    domain = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    
    prizeAmount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    nonMonetaryRewards = models.TextField(blank=True, help_text="Describe any non-monetary rewards.")
    deadline = models.DateField(null=True, blank=True) # Changed to DateField to match JSON
    benefits = models.TextField(blank=True)

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    website = models.URLField(max_length=255, blank=True)
    organizer = models.CharField(max_length=150, blank=True)

    timeCommitment = models.CharField(max_length=100, blank=True)
    teamRequirement = models.CharField(max_length=20, choices=TEAM_CHOICES, default='Both')
    targetAudience = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'competition_details'

    def __str__(self):
        return self.title
