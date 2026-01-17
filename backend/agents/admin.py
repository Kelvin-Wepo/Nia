from django.contrib import admin
from .models import AgentDecision, AgentPerformanceMetric, LearningRecord, AgentExperiment


@admin.register(AgentDecision)
class AgentDecisionAdmin(admin.ModelAdmin):
    list_display = ['user', 'decision_type', 'confidence_score', 'model_name', 'created_at']
    list_filter = ['decision_type', 'model_name', 'created_at']
    search_fields = ['user__username', 'decision', 'rationale']
    readonly_fields = ['created_at', 'opik_trace_id', 'opik_span_id']


@admin.register(AgentPerformanceMetric)
class AgentPerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['decision', 'was_implemented', 'user_satisfaction', 'effectiveness_score', 'response_time_ms']
    list_filter = ['was_implemented', 'user_satisfaction']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LearningRecord)
class LearningRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'insight_type', 'confidence', 'is_validated', 'success_rate']
    list_filter = ['insight_type', 'is_validated', 'created_at']
    search_fields = ['user__username', 'insight_description']


@admin.register(AgentExperiment)
class AgentExperimentAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'started_at', 'ended_at', 'winner']
    list_filter = ['is_active', 'started_at']
    search_fields = ['name', 'description', 'hypothesis']
