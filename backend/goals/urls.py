from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, MilestoneViewSet, ProgressUpdateViewSet, SetbackViewSet

router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'milestones', MilestoneViewSet, basename='milestone')
router.register(r'progress-updates', ProgressUpdateViewSet, basename='progress-update')
router.register(r'setbacks', SetbackViewSet, basename='setback')

urlpatterns = [
    path('', include(router.urls)),
]
