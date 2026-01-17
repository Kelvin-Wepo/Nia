from django.contrib import admin
from .models import Goal, Milestone, ProgressUpdate, Setback


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'progress_percentage', 'target_date']
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'is_completed']
    list_filter = ['is_completed', 'target_date']
    search_fields = ['title', 'goal__title']


@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ['goal', 'progress_percentage', 'mood', 'created_at']
    list_filter = ['mood', 'created_at']
    search_fields = ['goal__title', 'update_text']
    readonly_fields = ['created_at']


@admin.register(Setback)
class SetbackAdmin(admin.ModelAdmin):
    list_display = ['goal', 'severity', 'setback_type', 'is_resolved', 'occurred_at']
    list_filter = ['severity', 'is_resolved', 'setback_type']
    search_fields = ['goal__title', 'description']
    readonly_fields = ['occurred_at']
