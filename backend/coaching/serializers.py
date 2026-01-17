from rest_framework import serializers
from .models import CoachingSession, Message, CoachingStrategy, Intervention


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['timestamp']


class CoachingSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = CoachingSession
        fields = '__all__'
        read_only_fields = ['user', 'started_at', 'completed_at', 'reasoning_chain']


class CoachingStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingStrategy
        fields = '__all__'
        read_only_fields = ['success_rate', 'usage_count', 'created_at', 'updated_at']


class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'decision_reasoning', 'confidence_level']


class InterventionFeedbackSerializer(serializers.Serializer):
    was_helpful = serializers.BooleanField()
    user_feedback = serializers.CharField(allow_blank=True, required=False)
