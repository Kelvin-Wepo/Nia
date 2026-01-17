from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AgentDecisionViewSet, AgentPerformanceMetricViewSet,
    LearningRecordViewSet, AgentExperimentViewSet, AIServiceViewSet
)

router = DefaultRouter()
router.register(r'decisions', AgentDecisionViewSet, basename='decision')
router.register(r'metrics', AgentPerformanceMetricViewSet, basename='metric')
router.register(r'learning', LearningRecordViewSet, basename='learning')
router.register(r'experiments', AgentExperimentViewSet, basename='experiment')
router.register(r'ai', AIServiceViewSet, basename='ai')

urlpatterns = [
    path('', include(router.urls)),
]
