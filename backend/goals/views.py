from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Goal, Milestone, ProgressUpdate, Setback
from .serializers import (
    GoalSerializer, GoalCreateSerializer, GoalUpdateSerializer,
    MilestoneSerializer, ProgressUpdateSerializer, SetbackSerializer
)


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'category']
    
    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GoalCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GoalUpdateSerializer
        return GoalSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_milestone(self, request, pk=None):
        """Add a milestone to a goal"""
        goal = self.get_object()
        serializer = MilestoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(goal=goal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_progress(self, request, pk=None):
        """Add a progress update to a goal"""
        goal = self.get_object()
        serializer = ProgressUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        progress_update = serializer.save(goal=goal)
        
        # Update goal progress
        goal.progress_percentage = progress_update.progress_percentage
        goal.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def report_setback(self, request, pk=None):
        """Report a setback for a goal"""
        goal = self.get_object()
        serializer = SetbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(goal=goal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active goals"""
        goals = self.get_queryset().filter(status='active')
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get goal statistics for the user"""
        queryset = self.get_queryset()
        stats = {
            'total_goals': queryset.count(),
            'active_goals': queryset.filter(status='active').count(),
            'completed_goals': queryset.filter(status='completed').count(),
            'paused_goals': queryset.filter(status='paused').count(),
            'average_progress': queryset.filter(status='active').aggregate(
                avg_progress=models.Avg('progress_percentage')
            )['avg_progress'] or 0,
        }
        return Response(stats)


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Milestone.objects.filter(goal__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a milestone as completed"""
        milestone = self.get_object()
        milestone.is_completed = True
        milestone.completed_date = timezone.now().date()
        milestone.save()
        return Response(MilestoneSerializer(milestone).data)


class ProgressUpdateViewSet(viewsets.ModelViewSet):
    queryset = ProgressUpdate.objects.all()
    serializer_class = ProgressUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ProgressUpdate.objects.filter(goal__user=self.request.user)


class SetbackViewSet(viewsets.ModelViewSet):
    queryset = Setback.objects.all()
    serializer_class = SetbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Setback.objects.filter(goal__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark a setback as resolved"""
        setback = self.get_object()
        setback.is_resolved = True
        setback.resolved_at = timezone.now()
        setback.resolution_strategy = request.data.get('resolution_strategy', '')
        setback.save()
        return Response(SetbackSerializer(setback).data)


from django.db import models
from django.utils import timezone
