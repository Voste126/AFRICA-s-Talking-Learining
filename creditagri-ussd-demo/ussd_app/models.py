"""
USSD Application Models

This module implements models for:
- USSD response logging
- Beekeeper session management
- Risk profiling
- Claims management
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class BeekeeperSession(models.Model):
    """
    Stores USSD session information for beekeepers.
    Tracks user interactions and responses during the USSD session.
    """
    session_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    inputs = models.JSONField(default=dict, help_text="Stores all user inputs during the session")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Beekeeper Session: {self.phone_number} at {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class RiskProfile(models.Model):
    """
    Stores risk assessment results for beekeepers.
    Includes risk score, level, and insurance details.
    """
    RISK_LEVELS = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('High', 'High')
    ]

    session = models.ForeignKey(
        BeekeeperSession,
        on_delete=models.CASCADE,
        related_name='risk_profiles'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Risk score from 0-100"
    )
    level = models.CharField(
        max_length=10,
        choices=RISK_LEVELS,
        help_text="Risk level based on score"
    )
    premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Insurance premium amount"
    )
    cover_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total insurance coverage amount"
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Risk Profile: {self.session.phone_number} - {self.level}"

    class Meta:
        ordering = ['-generated_at']


class Claim(models.Model):
    """
    Stores insurance claim information.
    Tracks claim status and related documentation.
    """
    CLAIM_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    profile = models.ForeignKey(
        RiskProfile,
        on_delete=models.CASCADE,
        related_name='claims'
    )
    image_url = models.URLField(
        help_text="URL to the claim evidence image"
    )
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="AI confidence score for claim validation (0-1)"
    )
    status = models.CharField(
        max_length=10,
        choices=CLAIM_STATUS,
        default='pending',
        help_text="Current status of the claim"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim: {self.profile.session.phone_number} - {self.status}"

    class Meta:
        ordering = ['-created_at']


