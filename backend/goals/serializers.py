from rest_framework import serializers
from .models import Goal, Milestone, ProgressUpdate, Setback


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressUpdate
        fields = '__all__'
        read_only_fields = ['created_at', 'sentiment_score', 'key_insights']


class SetbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setback
        fields = '__all__'
        read_only_fields = ['occurred_at', 'ai_recovery_plan', 'similar_past_setbacks']


class GoalSerializer(serializers.ModelSerializer):
    milestones = MilestoneSerializer(many=True, read_only=True)
    progress_updates = ProgressUpdateSerializer(many=True, read_only=True)
    setbacks = SetbackSerializer(many=True, read_only=True)
    
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = [
            'user', 'created_at', 'updated_at', 'predicted_completion_date',
            'risk_factors', 'success_likelihood', 'current_strategy',
            'strategy_adjustments_count'
        ]


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'title', 'description', 'category', 'tags',
            'priority', 'start_date', 'target_date'
        ]


class GoalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            'title', 'description', 'category', 'tags',
            'status', 'priority', 'target_date', 'progress_percentage'
        ]
