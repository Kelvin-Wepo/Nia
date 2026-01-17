from django.db import models
from django.contrib.auth import get_user_model
from goals.models import Goal

User = get_user_model()


class AgentDecision(models.Model):
    """
    Represents a decision made by the AI agent with transparent reasoning.
    """
    DECISION_TYPE_CHOICES = [
        ('strategy_selection', 'Strategy Selection'),
        ('intervention_trigger', 'Intervention Trigger'),
        ('goal_adjustment', 'Goal Adjustment'),
        ('milestone_suggestion', 'Milestone Suggestion'),
        ('recovery_plan', 'Recovery Plan'),
        ('encouragement', 'Encouragement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_decisions')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_decisions')
    
    decision_type = models.CharField(max_length=50, choices=DECISION_TYPE_CHOICES)
    
    # Input context
    context = models.JSONField()
    user_state = models.JSONField()
    
    # Decision output
    decision = models.TextField()
    rationale = models.TextField()
    
    # Reasoning chain (transparent AI)
    reasoning_steps = models.JSONField(default=list)
    alternatives_considered = models.JSONField(default=list)
    
    # Confidence and metrics
    confidence_score = models.FloatField()
    risk_assessment = models.JSONField(default=dict)
    
    # Model information
    model_name = models.CharField(max_length=100)
    model_version = models.CharField(max_length=50)
    
    # Opik tracking
    opik_trace_id = models.CharField(max_length=255, blank=True)
    opik_span_id = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'agent_decisions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['decision_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.decision_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class AgentPerformanceMetric(models.Model):
    """
    Tracks performance metrics for agent decisions.
    """
    decision = models.OneToOneField(AgentDecision, on_delete=models.CASCADE, related_name='metrics')
    
    # Outcome tracking
    was_implemented = models.BooleanField(default=False)
    user_satisfaction = models.IntegerField(null=True, blank=True)  # 1-5 scale
    effectiveness_score = models.FloatField(null=True, blank=True)  # 0.0-1.0
    
    # Timing metrics
    response_time_ms = models.IntegerField()
    
    # User feedback
    user_feedback = models.TextField(blank=True)
    feedback_timestamp = models.DateTimeField(null=True, blank=True)
    
    # A/B testing
    variant = models.CharField(max_length=50, blank=True)
    control_group = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agent_performance_metrics'
    
    def __str__(self):
        return f"Metrics for {self.decision}"


class LearningRecord(models.Model):
    """
    Records what the AI learns from user interactions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_records')
    
    # What was learned
    insight_type = models.CharField(max_length=100)
    insight_description = models.TextField()
    
    # Evidence
    supporting_data = models.JSONField()
    confidence = models.FloatField()
    
    # Application
    applied_to_decisions = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validation_method = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_records'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.insight_type}"


class AgentExperiment(models.Model):
    """
    Represents A/B experiments for testing different agent strategies.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    hypothesis = models.TextField()
    
    # Experiment configuration
    variants = models.JSONField()  # List of variant configurations
    allocation = models.JSONField()  # Traffic allocation per variant
    
    # Metrics to track
    success_metrics = models.JSONField()
    
    # Status
    is_active = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Results
    results = models.JSONField(default=dict, blank=True)
    winner = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agent_experiments'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
