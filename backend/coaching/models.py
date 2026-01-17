from django.db import models
from django.contrib.auth import get_user_model
from goals.models import Goal

User = get_user_model()


class CoachingSession(models.Model):
    """
    Represents a coaching interaction between the AI and user.
    """
    SESSION_TYPE_CHOICES = [
        ('check_in', 'Check-in'),
        ('goal_setting', 'Goal Setting'),
        ('setback_recovery', 'Setback Recovery'),
        ('strategy_adjustment', 'Strategy Adjustment'),
        ('celebration', 'Celebration'),
        ('reflection', 'Reflection'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coaching_sessions')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='coaching_sessions')
    
    session_type = models.CharField(max_length=50, choices=SESSION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    
    # Session context
    context = models.JSONField(default=dict, blank=True)
    user_state = models.JSONField(default=dict, blank=True)  # mood, energy, confidence
    
    # Session outcome
    outcome_summary = models.TextField(blank=True)
    action_items = models.JSONField(default=list, blank=True)
    insights_gained = models.JSONField(default=list, blank=True)
    
    # AI metrics
    agent_confidence = models.FloatField(default=0.0)  # 0.0 to 1.0
    reasoning_chain = models.JSONField(default=list, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'coaching_sessions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.session_type} - {self.started_at.strftime('%Y-%m-%d')}"


class Message(models.Model):
    """
    Represents a message in a coaching conversation.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(CoachingSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    # AI reasoning (for assistant messages)
    reasoning = models.TextField(blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.role} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class CoachingStrategy(models.Model):
    """
    Represents different coaching strategies that can be applied.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    
    # When to use this strategy
    applicable_situations = models.JSONField(default=list, blank=True)
    user_personas = models.JSONField(default=list, blank=True)
    
    # Strategy parameters
    parameters = models.JSONField(default=dict, blank=True)
    
    # Effectiveness metrics
    success_rate = models.FloatField(default=0.0)
    usage_count = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coaching_strategies'
        ordering = ['-success_rate']
    
    def __str__(self):
        return self.name


class Intervention(models.Model):
    """
    Represents a coaching intervention triggered by the AI.
    """
    INTERVENTION_TYPE_CHOICES = [
        ('motivational', 'Motivational'),
        ('corrective', 'Corrective'),
        ('supportive', 'Supportive'),
        ('challenging', 'Challenging'),
        ('informational', 'Informational'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interventions')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='interventions')
    
    intervention_type = models.CharField(max_length=50, choices=INTERVENTION_TYPE_CHOICES)
    trigger_reason = models.TextField()
    
    # Intervention content
    message = models.TextField()
    recommended_actions = models.JSONField(default=list, blank=True)
    
    # AI decision making
    decision_reasoning = models.TextField()
    confidence_level = models.FloatField()
    alternative_approaches = models.JSONField(default=list, blank=True)
    
    # Effectiveness tracking
    was_helpful = models.BooleanField(null=True, blank=True)
    user_feedback = models.TextField(blank=True)
    outcome = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'interventions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.intervention_type} for {self.goal.title}"
