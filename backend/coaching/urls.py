from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CoachingSessionViewSet, MessageViewSet,
    CoachingStrategyViewSet, InterventionViewSet
)

router = DefaultRouter()
router.register(r'sessions', CoachingSessionViewSet, basename='session')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'strategies', CoachingStrategyViewSet, basename='strategy')
router.register(r'interventions', InterventionViewSet, basename='intervention')

urlpatterns = [
    path('', include(router.urls)),
]
