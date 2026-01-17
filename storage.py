"""
Simple storage system for goals, progress, and user data.
"""
import json
import os
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from models import (
    Goal, ProgressUpdate, Setback, UserBehaviorProfile, 
    GoalStatus, CoachingDecision
)


class DataStore:
    """Simple JSON-based data storage."""
    
    def __init__(self, data_dir: str = "user_data"):
        """Initialize data store with specified directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def _get_user_file(self, user_id: str, data_type: str) -> Path:
        """Get path to user data file."""
        user_dir = self.data_dir / user_id
        user_dir.mkdir(exist_ok=True)
        return user_dir / f"{data_type}.json"
    
    def save_goal(self, goal: Goal, user_id: str):
        """Save a goal."""
        goals = self.load_goals(user_id)
        
        # Update or add goal
        existing = False
        for i, g in enumerate(goals):
            if g.id == goal.id:
                goals[i] = goal
                existing = True
                break
        
        if not existing:
            goals.append(goal)
        
        file_path = self._get_user_file(user_id, "goals")
        with open(file_path, 'w') as f:
            json.dump([g.model_dump() for g in goals], f, indent=2, default=str)
    
    def load_goals(self, user_id: str) -> List[Goal]:
        """Load all goals for a user."""
        file_path = self._get_user_file(user_id, "goals")
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return [Goal(**g) for g in data]
    
    def get_goal(self, goal_id: str, user_id: str) -> Optional[Goal]:
        """Get a specific goal."""
        goals = self.load_goals(user_id)
        for goal in goals:
            if goal.id == goal_id:
                return goal
        return None
    
    def save_progress(self, progress: ProgressUpdate, user_id: str):
        """Save a progress update."""
        updates = self.load_progress(user_id, progress.goal_id)
        updates.append(progress)
        
        file_path = self._get_user_file(user_id, f"progress_{progress.goal_id}")
        with open(file_path, 'w') as f:
            json.dump([p.model_dump() for p in updates], f, indent=2, default=str)
    
    def load_progress(
        self, 
        user_id: str, 
        goal_id: str, 
        limit: Optional[int] = None
    ) -> List[ProgressUpdate]:
        """Load progress updates for a goal."""
        file_path = self._get_user_file(user_id, f"progress_{goal_id}")
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            updates = [ProgressUpdate(**p) for p in data]
            
            if limit:
                return updates[-limit:]
            return updates
    
    def save_setback(self, setback: Setback, user_id: str):
        """Save a setback."""
        setbacks = self.load_setbacks(user_id, setback.goal_id)
        
        # Update or add setback
        existing = False
        for i, s in enumerate(setbacks):
            if s.id == setback.id:
                setbacks[i] = setback
                existing = True
                break
        
        if not existing:
            setbacks.append(setback)
        
        file_path = self._get_user_file(user_id, f"setbacks_{setback.goal_id}")
        with open(file_path, 'w') as f:
            json.dump([s.model_dump() for s in setbacks], f, indent=2, default=str)
    
    def load_setbacks(self, user_id: str, goal_id: str) -> List[Setback]:
        """Load setbacks for a goal."""
        file_path = self._get_user_file(user_id, f"setbacks_{goal_id}")
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return [Setback(**s) for s in data]
    
    def save_behavior_profile(self, profile: UserBehaviorProfile):
        """Save user behavior profile."""
        file_path = self._get_user_file(profile.user_id, "behavior_profile")
        with open(file_path, 'w') as f:
            json.dump(profile.model_dump(), f, indent=2, default=str)
    
    def load_behavior_profile(self, user_id: str) -> Optional[UserBehaviorProfile]:
        """Load user behavior profile."""
        file_path = self._get_user_file(user_id, "behavior_profile")
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            return UserBehaviorProfile(**data)
    
    def save_decision(self, decision: CoachingDecision, user_id: str):
        """Save a coaching decision for transparency."""
        decisions = self.load_decisions(user_id)
        decisions.append(decision)
        
        file_path = self._get_user_file(user_id, "decisions")
        with open(file_path, 'w') as f:
            json.dump([d.model_dump() for d in decisions], f, indent=2, default=str)
    
    def load_decisions(
        self, 
        user_id: str, 
        limit: Optional[int] = None
    ) -> List[CoachingDecision]:
        """Load coaching decisions."""
        file_path = self._get_user_file(user_id, "decisions")
        
        if not file_path.exists():
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            decisions = [CoachingDecision(**d) for d in data]
            
            if limit:
                return decisions[-limit:]
            return decisions
