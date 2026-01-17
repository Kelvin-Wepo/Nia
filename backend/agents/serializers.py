from rest_framework import serializers
from .models import AgentDecision, AgentPerformanceMetric, LearningRecord, AgentExperiment


class AgentDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDecision
        fields = '__all__'
        read_only_fields = [
            'user', 'created_at', 'opik_trace_id', 'opik_span_id',
            'model_name', 'model_version'
        ]


class AgentPerformanceMetricSerializer(serializers.ModelSerializer):
    decision_details = AgentDecisionSerializer(source='decision', read_only=True)
    
    class Meta:
        model = AgentPerformanceMetric
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class LearningRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningRecord
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class AgentExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExperiment
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
