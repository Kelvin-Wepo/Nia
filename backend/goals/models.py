from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Goal(models.Model):
    """
    Represents a user's goal with adaptive tracking.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Goal categorization
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Status and priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Timeline
    start_date = models.DateField()
    target_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Progress tracking
    progress_percentage = models.IntegerField(default=0)
    is_on_track = models.BooleanField(default=True)
    
    # AI-driven insights
    predicted_completion_date = models.DateField(null=True, blank=True)
    risk_factors = models.JSONField(default=list, blank=True)
    success_likelihood = models.FloatField(default=0.5)  # 0.0 to 1.0
    
    # Adaptive strategy
    current_strategy = models.JSONField(default=dict, blank=True)
    strategy_adjustments_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'goals'
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Milestone(models.Model):
    """
    Represents a milestone/sub-goal within a larger goal.
    """
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Timeline
    target_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'milestones'
        ordering = ['order', 'target_date']
    
    def __str__(self):
        return f"{self.goal.title} - {self.title}"


class ProgressUpdate(models.Model):
    """
    Tracks progress updates for goals.
    """
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='progress_updates')
    update_text = models.TextField()
    progress_percentage = models.IntegerField()
    
    # Sentiment and mood
    mood = models.CharField(
        max_length=20,
        choices=[
            ('motivated', 'Motivated'),
            ('neutral', 'Neutral'),
            ('struggling', 'Struggling'),
            ('frustrated', 'Frustrated'),
            ('confident', 'Confident'),
        ],
        default='neutral'
    )
    
    # Attachments (images, documents)
    attachments = models.JSONField(default=list, blank=True)
    
    # AI analysis
    sentiment_score = models.FloatField(null=True, blank=True)  # -1.0 to 1.0
    key_insights = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'progress_updates'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.goal.title} - Update {self.created_at.strftime('%Y-%m-%d')}"


class Setback(models.Model):
    """
    Represents setbacks or challenges encountered while pursuing a goal.
    """
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ]
    
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='setbacks')
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='moderate')
    
    # Categorization
    setback_type = models.CharField(max_length=100)
    root_causes = models.JSONField(default=list, blank=True)
    
    # Recovery
    is_resolved = models.BooleanField(default=False)
    resolution_strategy = models.TextField(blank=True)
    recovery_actions = models.JSONField(default=list, blank=True)
    
    # AI-driven recovery
    ai_recovery_plan = models.JSONField(default=dict, blank=True)
    similar_past_setbacks = models.JSONField(default=list, blank=True)
    
    # Timeline
    occurred_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'setbacks'
        ordering = ['-occurred_at']
    
    def __str__(self):
        return f"{self.goal.title} - Setback ({self.severity})"
