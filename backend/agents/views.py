from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from .models import AgentDecision, AgentPerformanceMetric, LearningRecord, AgentExperiment
from .serializers import (
    AgentDecisionSerializer, AgentPerformanceMetricSerializer,
    LearningRecordSerializer, AgentExperimentSerializer
)
from .gemini_service import GeminiService
from .opik_service import OpikService


class AgentDecisionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing agent decisions and their transparent reasoning.
    """
    queryset = AgentDecision.objects.all()
    serializer_class = AgentDecisionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AgentDecision.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent agent decisions"""
        decisions = self.get_queryset()[:20]
        serializer = self.get_serializer(decisions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get decisions grouped by type"""
        decision_type = request.query_params.get('type')
        if decision_type:
            decisions = self.get_queryset().filter(decision_type=decision_type)
        else:
            decisions = self.get_queryset()
        
        serializer = self.get_serializer(decisions, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get decision statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_decisions': queryset.count(),
            'decisions_by_type': dict(
                queryset.values('decision_type').annotate(count=Count('id')).values_list('decision_type', 'count')
            ),
            'average_confidence': queryset.aggregate(avg_conf=Avg('confidence_score'))['avg_conf'] or 0,
            'most_common_model': queryset.values('model_name').annotate(
                count=Count('id')
            ).order_by('-count').first()
        }
        
        return Response(stats)


class AgentPerformanceMetricViewSet(viewsets.ModelViewSet):
    """
    ViewSet for tracking and viewing agent performance metrics.
    """
    queryset = AgentPerformanceMetric.objects.all()
    serializer_class = AgentPerformanceMetricSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AgentPerformanceMetric.objects.filter(decision__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get performance summary"""
        queryset = self.get_queryset()
        
        summary = {
            'total_tracked': queryset.count(),
            'implementation_rate': queryset.filter(was_implemented=True).count() / queryset.count() if queryset.count() > 0 else 0,
            'average_satisfaction': queryset.exclude(user_satisfaction__isnull=True).aggregate(
                avg_sat=Avg('user_satisfaction')
            )['avg_sat'] or 0,
            'average_effectiveness': queryset.exclude(effectiveness_score__isnull=True).aggregate(
                avg_eff=Avg('effectiveness_score')
            )['avg_eff'] or 0,
            'average_response_time': queryset.aggregate(
                avg_time=Avg('response_time_ms')
            )['avg_time'] or 0
        }
        
        return Response(summary)


class LearningRecordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing what the AI has learned about the user.
    """
    queryset = LearningRecord.objects.all()
    serializer_class = LearningRecordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LearningRecord.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def validated(self, request):
        """Get validated learning records"""
        records = self.get_queryset().filter(is_validated=True)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)


class AgentExperimentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing active agent experiments.
    """
    queryset = AgentExperiment.objects.filter(is_active=True)
    serializer_class = AgentExperimentSerializer
    permission_classes = [IsAuthenticated]


class AIServiceViewSet(viewsets.ViewSet):
    """
    ViewSet for AI service interactions (Gemini).
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gemini_service = GeminiService()
        self.opik_service = OpikService()
    
    @action(detail=False, methods=['post'])
    def generate_response(self, request):
        """Generate an AI coaching response"""
        user_message = request.data.get('message', '')
        context = request.data.get('context', {})
        coaching_style = request.user.coaching_style_preference
        
        result = self.gemini_service.generate_coaching_response(
            user_message=user_message,
            context=context,
            coaching_style=coaching_style
        )
        
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def analyze_setback(self, request):
        """Analyze a setback and provide recovery plan"""
        setback_description = request.data.get('description', '')
        goal_id = request.data.get('goal_id')
        
        # Get user history and goal context
        user_history = {
            'typical_setback_patterns': request.user.typical_setback_patterns,
            'success_triggers': request.user.success_triggers
        }
        
        from goals.models import Goal
        try:
            goal = Goal.objects.get(id=goal_id, user=request.user)
            goal_context = {
                'title': goal.title,
                'progress_percentage': goal.progress_percentage,
                'priority': goal.priority
            }
        except Goal.DoesNotExist:
            return Response(
                {'error': 'Goal not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        result = self.gemini_service.analyze_setback(
            setback_description=setback_description,
            user_history=user_history,
            goal_context=goal_context
        )
        
        return Response(result)
    
    @action(detail=False, methods=['post'])
    def suggest_strategy(self, request):
        """Suggest strategy adjustments for a goal"""
        goal_id = request.data.get('goal_id')
        
        from goals.models import Goal, ProgressUpdate
        try:
            goal = Goal.objects.get(id=goal_id, user=request.user)
            recent_progress = list(
                ProgressUpdate.objects.filter(goal=goal).order_by('-created_at')[:5]
                .values('progress_percentage', 'mood', 'created_at')
            )
            
            goal_dict = {
                'title': goal.title,
                'current_strategy': goal.current_strategy,
                'progress_percentage': goal.progress_percentage
            }
            
            user_behavior = {
                'typical_setback_patterns': request.user.typical_setback_patterns,
                'success_triggers': request.user.success_triggers
            }
            
            result = self.gemini_service.suggest_strategy_adjustment(
                goal=goal_dict,
                recent_progress=recent_progress,
                user_behavior=user_behavior
            )
            
            return Response(result)
            
        except Goal.DoesNotExist:
            return Response(
                {'error': 'Goal not found'},
                status=status.HTTP_404_NOT_FOUND
            )
