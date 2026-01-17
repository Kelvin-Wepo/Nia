"""
AI Agent for goal coaching with transparent reasoning and behavior adaptation.
"""
import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

from models import (
    Goal, UserBehaviorProfile, Setback, SetbackType, 
    ProgressUpdate, CoachingDecision, GoalStatus
)


class NiaCoachingAgent:
    """
    Agentic AI coach that adapts to user behavior, recovers from setbacks,
    and provides transparent reasoning for all decisions.
    """
    
    def __init__(self, user_id: str, use_mock: bool = False):
        """
        Initialize the coaching agent.
        
        Args:
            user_id: Unique identifier for the user
            use_mock: If True, use mock AI responses instead of OpenAI API
        """
        self.user_id = user_id
        self.use_mock = use_mock
        self.behavior_profile = UserBehaviorProfile(user_id=user_id)
        
        if not use_mock:
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    self.client = OpenAI(api_key=api_key)
                else:
                    print("Warning: No OpenAI API key found, using mock mode")
                    self.use_mock = True
            except ImportError:
                print("Warning: OpenAI library not installed, using mock mode")
                self.use_mock = True
    
    @staticmethod
    def _generate_id(prefix: str) -> str:
        """Generate a unique ID with a prefix."""
        return f"{prefix}_{uuid.uuid4()}"
    
    def detect_setback(
        self, 
        goal: Goal, 
        recent_updates: List[ProgressUpdate]
    ) -> Optional[Setback]:
        """
        Detect if a setback has occurred based on goal progress.
        
        Args:
            goal: The goal to check
            recent_updates: Recent progress updates
            
        Returns:
            Setback object if detected, None otherwise
        """
        reasoning = []
        
        # Check for missed milestones
        if goal.target_date and datetime.now() > goal.target_date:
            if goal.status != GoalStatus.COMPLETED:
                reasoning.append("Target date has passed without completion")
                return Setback(
                    id=self._generate_id("setback"),
                    goal_id=goal.id,
                    type=SetbackType.MISSED_MILESTONE,
                    description="Goal deadline passed without completion"
                )
        
        # Check for loss of motivation (no updates in a while)
        if recent_updates:
            last_update = recent_updates[-1]
            days_since_update = (datetime.now() - last_update.timestamp).days
            
            if days_since_update > 7:
                reasoning.append(f"No progress updates for {days_since_update} days")
                return Setback(
                    id=self._generate_id("setback"),
                    goal_id=goal.id,
                    type=SetbackType.LOSS_OF_MOTIVATION,
                    description=f"No activity for {days_since_update} days"
                )
            
            # Check for negative sentiment pattern
            recent_negative = sum(
                1 for u in recent_updates[-5:] if u.sentiment == "negative"
            )
            if recent_negative >= 3:
                reasoning.append("Multiple negative sentiment indicators")
                return Setback(
                    id=self._generate_id("setback"),
                    goal_id=goal.id,
                    type=SetbackType.EXTERNAL_OBSTACLE,
                    description="Consistent negative sentiment in recent updates"
                )
        
        return None
    
    def create_recovery_plan(
        self, 
        setback: Setback, 
        goal: Goal
    ) -> CoachingDecision:
        """
        Create a recovery plan for a detected setback.
        
        Args:
            setback: The detected setback
            goal: The associated goal
            
        Returns:
            CoachingDecision with recovery plan and reasoning
        """
        reasoning = []
        recovery_actions = []
        factors = {
            "setback_type": setback.type.value,
            "goal_status": goal.status.value,
            "user_motivation": self.behavior_profile.motivation_level,
            "typical_recovery_time": self.behavior_profile.typical_setback_recovery_days
        }
        
        reasoning.append(f"Detected setback type: {setback.type.value}")
        reasoning.append(f"User motivation level: {self.behavior_profile.motivation_level:.2f}")
        
        # Adapt recovery plan based on setback type and user profile
        if setback.type == SetbackType.MISSED_MILESTONE:
            reasoning.append("Missed milestone requires timeline reassessment")
            recovery_actions.append("Review and adjust goal timeline")
            recovery_actions.append("Break down remaining work into smaller milestones")
            
            if self.behavior_profile.motivation_level < 0.4:
                reasoning.append("Low motivation detected, adding encouragement")
                recovery_actions.append("Focus on small wins to rebuild momentum")
        
        elif setback.type == SetbackType.LOSS_OF_MOTIVATION:
            reasoning.append("Addressing motivation loss")
            
            if self.behavior_profile.response_to_encouragement == "positive":
                reasoning.append("User responds well to encouragement")
                recovery_actions.append("Revisit original goal motivation")
                recovery_actions.append("Celebrate any progress made so far")
            else:
                reasoning.append("User prefers direct approach")
                recovery_actions.append("Identify specific blockers")
                recovery_actions.append("Create concrete action plan")
            
            recovery_actions.append("Reduce scope to most important milestone")
        
        elif setback.type == SetbackType.EXTERNAL_OBSTACLE:
            reasoning.append("External obstacles require strategy adjustment")
            recovery_actions.append("Identify and document obstacles")
            recovery_actions.append("Develop alternative approaches")
            recovery_actions.append("Adjust expectations if needed")
        
        # Adapt based on engagement pattern
        if self.behavior_profile.engagement_pattern == "sporadic":
            reasoning.append("Sporadic engagement pattern - suggesting smaller commitments")
            recovery_actions.append("Set more frequent, smaller check-ins")
        
        decision = CoachingDecision(
            decision_id=self._generate_id("decision"),
            decision_type="setback_recovery",
            decision=f"Recovery plan for {setback.type.value}",
            reasoning=reasoning,
            factors_considered=factors,
            confidence=0.85
        )
        
        setback.recovery_actions = recovery_actions
        return decision
    
    def generate_coaching_advice(
        self,
        goal: Goal,
        recent_updates: List[ProgressUpdate],
        context: str = ""
    ) -> CoachingDecision:
        """
        Generate personalized coaching advice adapted to user behavior.
        
        Args:
            goal: The goal to provide advice for
            recent_updates: Recent progress updates
            context: Additional context for the advice
            
        Returns:
            CoachingDecision with advice and transparent reasoning
        """
        reasoning = []
        factors = {
            "goal_status": goal.status.value,
            "milestones_completed": len(goal.completed_milestones),
            "total_milestones": len(goal.milestones),
            "recent_update_count": len(recent_updates),
            "motivation_level": self.behavior_profile.motivation_level,
            "engagement_pattern": self.behavior_profile.engagement_pattern
        }
        
        # Analyze progress
        if goal.milestones:
            completion_rate = len(goal.completed_milestones) / len(goal.milestones)
            factors["completion_rate"] = completion_rate
            reasoning.append(f"Current completion rate: {completion_rate*100:.0f}%")
        else:
            completion_rate = 0.0
            reasoning.append("No milestones defined yet")
        
        # Adapt advice based on user behavior profile
        reasoning.append(f"User engagement pattern: {self.behavior_profile.engagement_pattern}")
        reasoning.append(f"User motivation level: {self.behavior_profile.motivation_level:.2f}")
        
        # Generate advice using mock or AI
        if self.use_mock:
            advice = self._generate_mock_advice(goal, completion_rate, recent_updates)
        else:
            advice = self._generate_ai_advice(goal, completion_rate, recent_updates, context)
        
        # Add reasoning based on adaptation
        if self.behavior_profile.motivation_level < 0.4:
            reasoning.append("Adapting tone for lower motivation - focusing on encouragement")
        elif self.behavior_profile.motivation_level > 0.7:
            reasoning.append("User highly motivated - providing advanced strategies")
        
        if recent_updates and recent_updates[-1].sentiment == "negative":
            reasoning.append("Recent negative sentiment - providing supportive guidance")
        
        decision = CoachingDecision(
            decision_id=self._generate_id("decision"),
            decision_type="advice",
            decision=advice,
            reasoning=reasoning,
            factors_considered=factors,
            confidence=0.8
        )
        
        return decision
    
    def _generate_mock_advice(
        self, 
        goal: Goal, 
        completion_rate: float, 
        recent_updates: List[ProgressUpdate]
    ) -> str:
        """Generate mock coaching advice for testing without API."""
        if completion_rate < 0.3:
            advice = (
                f"You're in the early stages of '{goal.title}'. "
                "Focus on building consistent habits and completing your first milestones. "
            )
            if self.behavior_profile.motivation_level < 0.5:
                advice += "Start with the smallest, easiest task to build momentum."
            else:
                advice += "You have good motivation - tackle a challenging milestone!"
        
        elif completion_rate < 0.7:
            advice = (
                f"Great progress on '{goal.title}'! You're over halfway there. "
                "Keep the momentum going by maintaining your current pace. "
            )
            if self.behavior_profile.engagement_pattern == "sporadic":
                advice += "Try to stay consistent with regular check-ins."
            
        else:
            advice = (
                f"Excellent work on '{goal.title}'! You're in the final stretch. "
                "Focus on completing the remaining milestones to achieve your goal."
            )
        
        return advice
    
    def _generate_ai_advice(
        self,
        goal: Goal,
        completion_rate: float,
        recent_updates: List[ProgressUpdate],
        context: str
    ) -> str:
        """Generate AI-powered coaching advice using OpenAI."""
        try:
            system_prompt = """You are Nia, an empathetic and adaptive AI goal coach. 
            Provide personalized, actionable advice to help users achieve their goals.
            Be encouraging but realistic. Adapt your tone and suggestions based on the user's 
            behavior profile and current situation."""
            
            user_prompt = f"""
            Goal: {goal.title}
            Description: {goal.description}
            Completion Rate: {completion_rate*100:.0f}%
            User Motivation: {self.behavior_profile.motivation_level:.2f}
            Engagement Pattern: {self.behavior_profile.engagement_pattern}
            
            Recent updates: {len(recent_updates)}
            {context}
            
            Provide brief, actionable coaching advice (2-3 sentences).
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating AI advice: {e}")
            return self._generate_mock_advice(goal, completion_rate, recent_updates)
    
    def update_behavior_profile(self, interaction_data: Dict[str, Any]):
        """
        Update the user's behavior profile based on new interaction.
        
        Args:
            interaction_data: Data from the interaction
        """
        self.behavior_profile.update_from_interaction(interaction_data)
    
    def get_transparency_report(self, decision: CoachingDecision) -> str:
        """
        Get a detailed transparency report for a decision.
        
        Args:
            decision: The decision to explain
            
        Returns:
            Formatted transparency report
        """
        return decision.explain()
