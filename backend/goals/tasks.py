"""
Celery tasks for goal management and monitoring.
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def check_goal_progress():
    """
    Periodic task to check goal progress and trigger interventions if needed.
    """
    from goals.models import Goal
    from agents.gemini_service import GeminiService
    from coaching.models import Intervention
    
    gemini = GeminiService()
    active_goals = Goal.objects.filter(status='active')
    
    for goal in active_goals:
        # Check if goal is falling behind
        days_until_target = (goal.target_date - timezone.now().date()).days
        expected_progress = 100 * (1 - days_until_target / ((goal.target_date - goal.start_date).days or 1))
        
        if goal.progress_percentage < expected_progress - 20:  # 20% behind
            # Trigger intervention
            trigger_coaching_intervention.delay(
                user_id=goal.user.id,
                goal_id=goal.id,
                trigger_reason="Goal progress is significantly behind schedule"
            )


@shared_task
def trigger_coaching_intervention(user_id: int, goal_id: int, trigger_reason: str):
    """
    Trigger a coaching intervention for a user/goal.
    """
    from goals.models import Goal
    from coaching.models import Intervention
    from agents.gemini_service import GeminiService
    from agents.opik_service import OpikService
    
    try:
        user = User.objects.get(id=user_id)
        goal = Goal.objects.get(id=goal_id, user=user)
        
        gemini = GeminiService()
        opik = OpikService()
        
        # Generate intervention
        user_state = {
            'coaching_style': user.coaching_style_preference,
            'timezone': user.timezone
        }
        
        goal_state = {
            'title': goal.title,
            'progress': goal.progress_percentage,
            'status': goal.status,
            'is_on_track': goal.is_on_track
        }
        
        intervention_data = gemini.generate_intervention(
            trigger=trigger_reason,
            user_state=user_state,
            goal_state=goal_state
        )
        
        # Create intervention record
        intervention = Intervention.objects.create(
            user=user,
            goal=goal,
            intervention_type=intervention_data.get('intervention_type', 'supportive'),
            trigger_reason=trigger_reason,
            message=intervention_data.get('message', ''),
            recommended_actions=intervention_data.get('recommended_actions', []),
            decision_reasoning=intervention_data.get('reasoning', ''),
            confidence_level=intervention_data.get('confidence', 0.5)
        )
        
        # Track with Opik
        opik.track_decision(
            decision_type='intervention_trigger',
            context={'trigger': trigger_reason, 'user_state': user_state, 'goal_state': goal_state},
            decision=intervention_data
        )
        
        # Send notification (implement notification system)
        # send_notification.delay(user_id, intervention.id)
        
        return intervention.id
        
    except Exception as e:
        print(f"Error triggering intervention: {e}")
        return None


@shared_task
def update_goal_predictions():
    """
    Update AI predictions for all active goals.
    """
    from goals.models import Goal, ProgressUpdate
    from agents.gemini_service import GeminiService
    
    gemini = GeminiService()
    active_goals = Goal.objects.filter(status='active')
    
    for goal in active_goals:
        recent_progress = list(
            ProgressUpdate.objects.filter(goal=goal)
            .order_by('-created_at')[:10]
            .values('progress_percentage', 'mood', 'created_at')
        )
        
        if recent_progress:
            # Calculate velocity and predict completion
            # Simple prediction based on recent progress
            progress_points = [(p['created_at'], p['progress_percentage']) for p in recent_progress]
            
            # Update risk factors
            setback_count = goal.setbacks.filter(
                occurred_at__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            if setback_count > 2:
                goal.risk_factors = ['frequent_setbacks', 'needs_strategy_adjustment']
            
            goal.save()


@shared_task
def analyze_user_behavior_patterns():
    """
    Analyze user behavior patterns and update learning records.
    """
    from users.models import UserBehaviorLog
    from agents.models import LearningRecord
    
    for user in User.objects.filter(is_active=True):
        # Get recent behavior logs
        recent_logs = UserBehaviorLog.objects.filter(
            user=user,
            timestamp__gte=timezone.now() - timedelta(days=30)
        )
        
        # Analyze patterns
        event_counts = {}
        for log in recent_logs:
            event_type = log.event_type
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Create learning records for significant patterns
        if event_counts:
            most_common_event = max(event_counts.items(), key=lambda x: x[1])
            
            LearningRecord.objects.get_or_create(
                user=user,
                insight_type='behavioral_pattern',
                defaults={
                    'insight_description': f"User frequently performs: {most_common_event[0]}",
                    'supporting_data': event_counts,
                    'confidence': 0.7,
                    'is_validated': False
                }
            )


@shared_task
def send_daily_check_ins():
    """
    Send daily check-in prompts to users who have that preference.
    """
    from coaching.models import CoachingSession
    
    users = User.objects.filter(
        is_active=True,
        preferred_check_in_frequency='daily'
    )
    
    for user in users:
        # Create a check-in session
        session = CoachingSession.objects.create(
            user=user,
            session_type='check_in',
            title=f"Daily Check-in - {timezone.now().strftime('%Y-%m-%d')}",
            context={'automated': True, 'frequency': 'daily'}
        )
        
        # Send notification
        # send_check_in_notification.delay(user.id, session.id)
