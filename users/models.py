# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import random
from django.utils import timezone

class CustomUser(AbstractUser):
    # --- Add these new fields ---
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry_time = models.DateTimeField(null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    # --- Keep the existing field ---
    date_of_birth = models.DateField(null=True, blank=True)

    def generate_otp(self):
        """Generates a 6-digit OTP and sets its expiry time."""
        self.email_otp = str(random.randint(100000, 999999))
        self.otp_expiry_time = timezone.now() + timezone.timedelta(minutes=10)
        self.save()

class UserProfile(models.Model):
    # This is the 'userId'. It links this profile to a specific user.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # --- New fields based on your updated schema ---
    primaryGoal = models.CharField(max_length=255, blank=True)
    availabilityTimeframe = models.CharField(max_length=150, blank=True)
    teamStatus = models.CharField(max_length=100, blank=True)
    experienceLevel = models.CharField(max_length=100, blank=True)
    projectTitle = models.CharField(max_length=255, blank=True)
    projectDescription = models.TextField(blank=True)
    domain = models.CharField(max_length=100, blank=True)
    # The 'keySkills' array is stored as text. The frontend will be responsible for parsing it.
    keySkills = models.TextField(blank=True, help_text="Store as a comma-separated string or JSON array string")
    projectStage = models.CharField(max_length=100, blank=True)
    
    # These fields will be automatically managed by Django.
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"