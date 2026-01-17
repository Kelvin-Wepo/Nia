from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import CoachingSession, Message, CoachingStrategy, Intervention
from .serializers import (
    CoachingSessionSerializer, MessageSerializer,
    CoachingStrategySerializer, InterventionSerializer,
    InterventionFeedbackSerializer
)


class CoachingSessionViewSet(viewsets.ModelViewSet):
    queryset = CoachingSession.objects.all()
    serializer_class = CoachingSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CoachingSession.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a coaching session as completed"""
        session = self.get_object()
        session.completed_at = timezone.now()
        
        # Calculate duration
        duration = (session.completed_at - session.started_at).total_seconds() / 60
        session.duration_minutes = int(duration)
        
        session.outcome_summary = request.data.get('outcome_summary', '')
        session.action_items = request.data.get('action_items', [])
        session.insights_gained = request.data.get('insights_gained', [])
        
        session.save()
        return Response(CoachingSessionSerializer(session).data)
    
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """Add a message to a coaching session"""
        session = self.get_object()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(session=session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent coaching sessions"""
        sessions = self.get_queryset()[:10]
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(session__user=self.request.user)


class CoachingStrategyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CoachingStrategy.objects.filter(is_active=True)
    serializer_class = CoachingStrategySerializer
    permission_classes = [IsAuthenticated]


class InterventionViewSet(viewsets.ModelViewSet):
    queryset = Intervention.objects.all()
    serializer_class = InterventionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Intervention.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """Provide feedback on an intervention"""
        intervention = self.get_object()
        serializer = InterventionFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        intervention.was_helpful = serializer.validated_data['was_helpful']
        intervention.user_feedback = serializer.validated_data.get('user_feedback', '')
        intervention.save()
        
        return Response(InterventionSerializer(intervention).data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending interventions (not yet rated)"""
        interventions = self.get_queryset().filter(was_helpful__isnull=True)
        serializer = self.get_serializer(interventions, many=True)
        return Response(serializer.data)
