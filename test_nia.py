"""
Tests for the Nia AI Goal Coaching Platform.
"""
import pytest
from datetime import datetime, timedelta
import os
import tempfile
import shutil

from models import (
    Goal, UserBehaviorProfile, Setback, SetbackType,
    ProgressUpdate, CoachingDecision, GoalStatus
)
from agent import NiaCoachingAgent
from storage import DataStore


class TestModels:
    """Test domain models."""
    
    def test_goal_creation(self):
        """Test creating a goal."""
        goal = Goal(
            id="test-1",
            title="Learn Python",
            description="Master Python programming",
            milestones=["Complete basics", "Build a project"]
        )
        
        assert goal.title == "Learn Python"
        assert goal.status == GoalStatus.ACTIVE
        assert len(goal.milestones) == 2
        assert len(goal.completed_milestones) == 0
    
    def test_behavior_profile_update(self):
        """Test behavior profile adaptation."""
        profile = UserBehaviorProfile(user_id="test_user")
        
        initial_motivation = profile.motivation_level
        profile.update_from_interaction({"motivation_indicator": 0.9})
        
        # Moving average formula: old * 0.7 + new * 0.3
        # 0.5 * 0.7 + 0.9 * 0.3 = 0.35 + 0.27 = 0.62
        assert profile.motivation_level > initial_motivation
        assert abs(profile.motivation_level - 0.62) < 0.01  # Check expected value
    
    def test_coaching_decision_explanation(self):
        """Test transparent reasoning in decisions."""
        decision = CoachingDecision(
            decision_id="test-decision",
            decision_type="advice",
            decision="Focus on small wins",
            reasoning=[
                "User motivation is low",
                "Small wins build momentum"
            ],
            factors_considered={"motivation": 0.3},
            confidence=0.8
        )
        
        explanation = decision.explain()
        
        assert "Focus on small wins" in explanation
        assert "User motivation is low" in explanation
        assert "80%" in explanation


class TestNiaCoachingAgent:
    """Test the AI coaching agent."""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent."""
        return NiaCoachingAgent(user_id="test_user", use_mock=True)
    
    @pytest.fixture
    def test_goal(self):
        """Create a test goal."""
        return Goal(
            id="goal-1",
            title="Write a book",
            description="Complete my first novel",
            target_date=datetime.now() + timedelta(days=30),
            milestones=["Outline", "First draft", "Editing", "Publishing"]
        )
    
    def test_setback_detection_missed_deadline(self, agent, test_goal):
        """Test detection of missed deadline setback."""
        # Set goal deadline in the past
        test_goal.target_date = datetime.now() - timedelta(days=1)
        test_goal.status = GoalStatus.ACTIVE
        
        setback = agent.detect_setback(test_goal, [])
        
        assert setback is not None
        assert setback.type == SetbackType.MISSED_MILESTONE
    
    def test_setback_detection_motivation_loss(self, agent, test_goal):
        """Test detection of motivation loss."""
        # Create old progress update
        old_update = ProgressUpdate(
            goal_id=test_goal.id,
            timestamp=datetime.now() - timedelta(days=10),
            progress_description="Started work"
        )
        
        setback = agent.detect_setback(test_goal, [old_update])
        
        assert setback is not None
        assert setback.type == SetbackType.LOSS_OF_MOTIVATION
    
    def test_setback_detection_negative_sentiment(self, agent, test_goal):
        """Test detection of negative sentiment pattern."""
        updates = [
            ProgressUpdate(
                goal_id=test_goal.id,
                progress_description="Struggling",
                sentiment="negative"
            )
            for _ in range(3)
        ]
        
        setback = agent.detect_setback(test_goal, updates)
        
        assert setback is not None
        assert setback.type == SetbackType.EXTERNAL_OBSTACLE
    
    def test_recovery_plan_generation(self, agent, test_goal):
        """Test recovery plan generation."""
        setback = Setback(
            id="setback-1",
            goal_id=test_goal.id,
            type=SetbackType.LOSS_OF_MOTIVATION,
            description="No updates for 10 days"
        )
        
        decision = agent.create_recovery_plan(setback, test_goal)
        
        assert decision.decision_type == "setback_recovery"
        assert len(decision.reasoning) > 0
        assert len(setback.recovery_actions) > 0
        assert "motivation" in decision.decision.lower() or len(setback.recovery_actions) > 0
    
    def test_coaching_advice_generation(self, agent, test_goal):
        """Test coaching advice generation."""
        updates = [
            ProgressUpdate(
                goal_id=test_goal.id,
                progress_description="Completed outline",
                sentiment="positive"
            )
        ]
        
        decision = agent.generate_coaching_advice(test_goal, updates)
        
        assert decision.decision_type == "advice"
        assert len(decision.reasoning) > 0
        assert len(decision.decision) > 0
        assert decision.confidence > 0
    
    def test_behavior_adaptation_low_motivation(self, agent, test_goal):
        """Test adaptation to low motivation."""
        agent.behavior_profile.motivation_level = 0.3
        
        updates = []
        decision = agent.generate_coaching_advice(test_goal, updates)
        
        # Should mention adaptation in reasoning
        reasoning_text = " ".join(decision.reasoning).lower()
        assert "motivation" in reasoning_text or "encouragement" in reasoning_text
    
    def test_behavior_profile_update(self, agent):
        """Test behavior profile updates."""
        initial_check_ins = len(agent.behavior_profile.preferred_check_in_times)
        
        agent.update_behavior_profile({
            "check_in_hour": 14,
            "motivation_indicator": 0.7
        })
        
        assert len(agent.behavior_profile.preferred_check_in_times) == initial_check_ins + 1
        assert 14 in agent.behavior_profile.preferred_check_in_times


class TestDataStore:
    """Test data storage."""
    
    @pytest.fixture
    def temp_store(self):
        """Create a temporary data store."""
        temp_dir = tempfile.mkdtemp()
        store = DataStore(data_dir=temp_dir)
        yield store
        shutil.rmtree(temp_dir)
    
    def test_save_and_load_goal(self, temp_store):
        """Test saving and loading goals."""
        goal = Goal(
            id="test-goal",
            title="Test Goal",
            description="Test description"
        )
        
        temp_store.save_goal(goal, "test_user")
        loaded_goals = temp_store.load_goals("test_user")
        
        assert len(loaded_goals) == 1
        assert loaded_goals[0].id == "test-goal"
        assert loaded_goals[0].title == "Test Goal"
    
    def test_save_and_load_progress(self, temp_store):
        """Test saving and loading progress updates."""
        progress = ProgressUpdate(
            goal_id="goal-1",
            progress_description="Made progress"
        )
        
        temp_store.save_progress(progress, "test_user")
        loaded_progress = temp_store.load_progress("test_user", "goal-1")
        
        assert len(loaded_progress) == 1
        assert loaded_progress[0].goal_id == "goal-1"
    
    def test_save_and_load_setback(self, temp_store):
        """Test saving and loading setbacks."""
        setback = Setback(
            id="setback-1",
            goal_id="goal-1",
            type=SetbackType.MISSED_MILESTONE,
            description="Missed deadline"
        )
        
        temp_store.save_setback(setback, "test_user")
        loaded_setbacks = temp_store.load_setbacks("test_user", "goal-1")
        
        assert len(loaded_setbacks) == 1
        assert loaded_setbacks[0].type == SetbackType.MISSED_MILESTONE
    
    def test_save_and_load_behavior_profile(self, temp_store):
        """Test saving and loading behavior profiles."""
        profile = UserBehaviorProfile(
            user_id="test_user",
            motivation_level=0.7,
            engagement_pattern="consistent"
        )
        
        temp_store.save_behavior_profile(profile)
        loaded_profile = temp_store.load_behavior_profile("test_user")
        
        assert loaded_profile is not None
        assert loaded_profile.user_id == "test_user"
        assert loaded_profile.motivation_level == 0.7
    
    def test_save_and_load_decisions(self, temp_store):
        """Test saving and loading decisions for transparency."""
        decision = CoachingDecision(
            decision_id="decision-1",
            decision_type="advice",
            decision="Test advice",
            reasoning=["Reason 1", "Reason 2"]
        )
        
        temp_store.save_decision(decision, "test_user")
        loaded_decisions = temp_store.load_decisions("test_user")
        
        assert len(loaded_decisions) == 1
        assert loaded_decisions[0].decision_id == "decision-1"


class TestTransparency:
    """Test transparency features."""
    
    def test_decision_has_reasoning(self):
        """Test that decisions include reasoning."""
        decision = CoachingDecision(
            decision_id="test",
            decision_type="advice",
            decision="Take a break",
            reasoning=[
                "User has been working consistently",
                "Rest improves long-term productivity"
            ],
            factors_considered={
                "consecutive_work_days": 7,
                "motivation_level": 0.6
            }
        )
        
        assert len(decision.reasoning) >= 2
        assert len(decision.factors_considered) > 0
        
        explanation = decision.explain()
        assert "Take a break" in explanation
        assert "consecutive_work_days" in explanation
    
    def test_setback_includes_recovery_actions(self):
        """Test that setbacks include recovery actions."""
        agent = NiaCoachingAgent(user_id="test", use_mock=True)
        
        setback = Setback(
            id="setback-1",
            goal_id="goal-1",
            type=SetbackType.LOSS_OF_MOTIVATION,
            description="No activity"
        )
        
        goal = Goal(
            id="goal-1",
            title="Test",
            description="Test goal"
        )
        
        decision = agent.create_recovery_plan(setback, goal)
        
        assert len(setback.recovery_actions) > 0
        assert len(decision.reasoning) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
