"""
Celery tasks for coaching session management.
"""

from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def process_coaching_message(session_id: int, message_content: str, role: str):
    """
    Process and store a coaching message.
    """
    from coaching.models import CoachingSession, Message
    
    try:
        session = CoachingSession.objects.get(id=session_id)
        
        message = Message.objects.create(
            session=session,
            role=role,
            content=message_content
        )
        
        return message.id
    except CoachingSession.DoesNotExist:
        return None


@shared_task
def generate_session_summary(session_id: int):
    """
    Generate a summary for a completed coaching session.
    """
    from coaching.models import CoachingSession
    from agents.gemini_service import GeminiService
    
    try:
        session = CoachingSession.objects.get(id=session_id)
        
        if not session.completed_at:
            return None
        
        gemini = GeminiService()
        
        # Get all messages from the session
        messages = session.messages.all().values('role', 'content', 'timestamp')
        conversation = [
            f"{msg['role']}: {msg['content']}" 
            for msg in messages
        ]
        
        # Generate summary using Gemini
        prompt = f"""
        Summarize this coaching session and extract key insights and action items.
        
        Conversation:
        {chr(10).join(conversation)}
        
        Provide:
        1. Brief summary (2-3 sentences)
        2. Key insights gained
        3. Action items discussed
        4. User's emotional state throughout
        
        Format as JSON with keys: summary, insights, action_items, user_state
        """
        
        # This would use the Gemini service to generate the summary
        # For now, we'll create a basic summary
        session.outcome_summary = f"Session with {len(messages)} messages"
        session.save()
        
        return session.id
        
    except CoachingSession.DoesNotExist:
        return None


@shared_task
def analyze_coaching_effectiveness():
    """
    Analyze the effectiveness of coaching sessions.
    """
    from coaching.models import CoachingSession, Intervention
    from agents.models import AgentPerformanceMetric
    
    # Get recent sessions
    recent_sessions = CoachingSession.objects.filter(
        completed_at__isnull=False,
        started_at__gte=timezone.now() - timezone.timedelta(days=30)
    )
    
    for session in recent_sessions:
        # Check if there were any related interventions
        if session.goal:
            interventions = Intervention.objects.filter(
                goal=session.goal,
                created_at__gte=session.started_at,
                created_at__lte=session.completed_at or timezone.now()
            )
            
            for intervention in interventions:
                # Check if metrics exist
                if not hasattr(intervention, 'metrics'):
                    # Create placeholder metrics
                    # In production, these would be calculated based on actual outcomes
                    pass
