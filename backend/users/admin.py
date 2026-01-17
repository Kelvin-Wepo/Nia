from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserBehaviorLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'coaching_style_preference', 'last_active', 'is_staff']
    list_filter = ['coaching_style_preference', 'preferred_check_in_frequency', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Coaching Preferences', {
            'fields': ('coaching_style_preference', 'preferred_check_in_frequency', 'timezone', 'bio')
        }),
        ('Behavioral Patterns', {
            'fields': ('typical_setback_patterns', 'success_triggers')
        }),
    )


@admin.register(UserBehaviorLog)
class UserBehaviorLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['user__username', 'user__email', 'event_type']
    readonly_fields = ['timestamp']
