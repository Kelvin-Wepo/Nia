from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Nia platform.
    Extends Django's AbstractUser to add coaching-specific fields.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Coaching preferences
    coaching_style_preference = models.CharField(
        max_length=50,
        choices=[
            ('supportive', 'Supportive'),
            ('direct', 'Direct'),
            ('analytical', 'Analytical'),
            ('motivational', 'Motivational'),
        ],
        default='supportive'
    )
    
    preferred_check_in_frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('biweekly', 'Bi-weekly'),
        ],
        default='weekly'
    )
    
    # Behavioral patterns (learned by AI over time)
    typical_setback_patterns = models.JSONField(default=dict, blank=True)
    success_triggers = models.JSONField(default=dict, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email


class UserBehaviorLog(models.Model):
    """
    Tracks user behavior patterns for AI learning.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behavior_logs')
    event_type = models.CharField(max_length=50)
    event_data = models.JSONField()
    context = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_behavior_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['event_type', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.event_type} - {self.timestamp}"
