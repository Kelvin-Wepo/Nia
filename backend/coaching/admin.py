from django.contrib import admin
from .models import CoachingSession, Message, CoachingStrategy, Intervention


@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'goal', 'started_at', 'duration_minutes']
    list_filter = ['session_type', 'started_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['started_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'timestamp']
    list_filter = ['role', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']


@admin.register(CoachingStrategy)
class CoachingStrategyAdmin(admin.ModelAdmin):
    list_display = ['name', 'success_rate', 'usage_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'intervention_type', 'was_helpful', 'created_at']
    list_filter = ['intervention_type', 'was_helpful', 'created_at']
    search_fields = ['user__username', 'goal__title', 'message']
    readonly_fields = ['created_at']
