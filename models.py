"""
Core domain models for the Nia AI Goal Coaching Platform.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class GoalStatus(str, Enum):
    """Status of a goal."""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    ABANDONED = "abandoned"


class SetbackType(str, Enum):
    """Types of setbacks users might experience."""
    MISSED_MILESTONE = "missed_milestone"
    LOSS_OF_MOTIVATION = "loss_of_motivation"
    EXTERNAL_OBSTACLE = "external_obstacle"
    SKILL_GAP = "skill_gap"
    TIME_CONSTRAINT = "time_constraint"


class Goal(BaseModel):
    """Represents a user goal."""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    id: str
    title: str
    description: str
    target_date: Optional[datetime] = None
    status: GoalStatus = GoalStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.now)
    milestones: List[str] = Field(default_factory=list)
    completed_milestones: List[str] = Field(default_factory=list)


class UserBehaviorProfile(BaseModel):
    """Tracks patterns in user behavior for adaptation."""
    user_id: str
    preferred_check_in_times: List[int] = Field(default_factory=list)  # Hours of day
    average_progress_rate: float = 0.0
    typical_setback_recovery_days: float = 7.0
    motivation_level: float = 0.5  # 0.0 to 1.0
    response_to_encouragement: str = "positive"  # positive, neutral, prefers_directness
    engagement_pattern: str = "consistent"  # consistent, sporadic, declining
    
    def update_from_interaction(self, interaction_data: Dict[str, Any]):
        """Update profile based on new interaction data."""
        if "check_in_hour" in interaction_data:
            self.preferred_check_in_times.append(interaction_data["check_in_hour"])
            # Keep only last 10
            self.preferred_check_in_times = self.preferred_check_in_times[-10:]
        
        if "motivation_indicator" in interaction_data:
            # Moving average
            self.motivation_level = (self.motivation_level * 0.7 + 
                                   interaction_data["motivation_indicator"] * 0.3)


class Setback(BaseModel):
    """Represents a setback in goal progress."""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    id: str
    goal_id: str
    type: SetbackType
    description: str
    detected_at: datetime = Field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    recovery_actions: List[str] = Field(default_factory=list)


class ProgressUpdate(BaseModel):
    """Tracks progress on a goal."""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    goal_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    progress_description: str
    milestone_completed: Optional[str] = None
    sentiment: str = "neutral"  # positive, neutral, negative


class CoachingDecision(BaseModel):
    """Represents a decision made by the AI coach with transparent reasoning."""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
    decision_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    decision_type: str  # advice, encouragement, strategy_change, setback_recovery
    decision: str
    reasoning: List[str]  # Step-by-step reasoning
    factors_considered: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.8  # 0.0 to 1.0
    
    def explain(self) -> str:
        """Generate human-readable explanation of the decision."""
        explanation = f"Decision: {self.decision}\n\n"
        explanation += "Reasoning:\n"
        for i, reason in enumerate(self.reasoning, 1):
            explanation += f"{i}. {reason}\n"
        explanation += f"\nConfidence: {self.confidence*100:.0f}%\n"
        if self.factors_considered:
            explanation += "\nFactors Considered:\n"
            for key, value in self.factors_considered.items():
                explanation += f"  - {key}: {value}\n"
        return explanation
