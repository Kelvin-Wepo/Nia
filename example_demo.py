"""
Example demonstration of Nia AI Goal Coaching Platform features.
"""
from datetime import datetime, timedelta
import uuid

from models import Goal, ProgressUpdate, GoalStatus
from agent import NiaCoachingAgent
from storage import DataStore


def demonstrate_nia():
    """Demonstrate key features of Nia."""
    print("=" * 70)
    print("Nia AI Goal Coaching Platform - Feature Demonstration")
    print("=" * 70)
    print()
    
    # Initialize
    user_id = "demo_user"
    agent = NiaCoachingAgent(user_id=user_id, use_mock=True)
    store = DataStore()
    
    # Feature 1: Create a Goal
    print("📝 Feature 1: Creating a Goal")
    print("-" * 70)
    
    goal = Goal(
        id=str(uuid.uuid4()),
        title="Launch a SaaS Product",
        description="Build and launch a SaaS product in 90 days",
        target_date=datetime.now() + timedelta(days=90),
        milestones=[
            "Complete market research",
            "Build MVP",
            "Get first 10 beta users",
            "Launch publicly"
        ]
    )
    
    store.save_goal(goal, user_id)
    print(f"✓ Created goal: {goal.title}")
    print(f"  Milestones: {len(goal.milestones)}")
    print(f"  Target date: {goal.target_date.strftime('%Y-%m-%d')}")
    print()
    
    # Feature 2: Track Progress & Adaptation
    print("📊 Feature 2: Tracking Progress (Behavior Adaptation)")
    print("-" * 70)
    
    # Simulate some progress updates
    updates = [
        ProgressUpdate(
            goal_id=goal.id,
            progress_description="Completed market research survey",
            milestone_completed="Complete market research",
            sentiment="positive"
        ),
        ProgressUpdate(
            goal_id=goal.id,
            progress_description="Started building MVP, made good progress",
            sentiment="positive"
        ),
        ProgressUpdate(
            goal_id=goal.id,
            progress_description="Feeling overwhelmed with technical challenges",
            sentiment="negative"
        ),
    ]
    
    for update in updates:
        store.save_progress(update, user_id)
        # Update behavior profile based on interaction
        motivation_map = {"positive": 0.8, "neutral": 0.5, "negative": 0.3}
        agent.update_behavior_profile({
            "check_in_hour": datetime.now().hour,
            "motivation_indicator": motivation_map[update.sentiment]
        })
    
    # Update goal with completed milestone
    goal.completed_milestones.append("Complete market research")
    store.save_goal(goal, user_id)
    
    print(f"✓ Recorded {len(updates)} progress updates")
    print(f"  Milestones completed: {len(goal.completed_milestones)}/{len(goal.milestones)}")
    print(f"  Behavior profile updated:")
    print(f"    - Motivation level: {agent.behavior_profile.motivation_level:.2f}")
    print(f"    - Engagement pattern: {agent.behavior_profile.engagement_pattern}")
    print()
    
    # Feature 3: Transparent AI Coaching
    print("🤖 Feature 3: AI Coaching with Transparent Reasoning")
    print("-" * 70)
    
    decision = agent.generate_coaching_advice(goal, updates)
    store.save_decision(decision, user_id)
    
    print("COACHING ADVICE:")
    print(f"  {decision.decision}")
    print()
    print("TRANSPARENT REASONING:")
    for i, reason in enumerate(decision.reasoning, 1):
        print(f"  {i}. {reason}")
    print()
    print(f"CONFIDENCE: {decision.confidence*100:.0f}%")
    print()
    print("FACTORS CONSIDERED:")
    for key, value in decision.factors_considered.items():
        print(f"  - {key}: {value}")
    print()
    
    # Feature 4: Setback Detection
    print("⚠️  Feature 4: Automatic Setback Detection")
    print("-" * 70)
    
    # Simulate a setback scenario - add negative updates
    negative_updates = [
        ProgressUpdate(
            goal_id=goal.id,
            progress_description="Still stuck on technical issues",
            sentiment="negative",
            timestamp=datetime.now() - timedelta(days=1)
        ),
        ProgressUpdate(
            goal_id=goal.id,
            progress_description="Not making progress, feeling discouraged",
            sentiment="negative",
            timestamp=datetime.now()
        ),
    ]
    
    for update in negative_updates:
        store.save_progress(update, user_id)
    
    all_updates = updates + negative_updates
    setback = agent.detect_setback(goal, all_updates)
    
    if setback:
        print(f"✓ Setback detected!")
        print(f"  Type: {setback.type.value}")
        print(f"  Description: {setback.description}")
        print()
        
        # Feature 5: Recovery Plan
        print("🔄 Feature 5: Personalized Recovery Plan")
        print("-" * 70)
        
        recovery_decision = agent.create_recovery_plan(setback, goal)
        store.save_setback(setback, user_id)
        store.save_decision(recovery_decision, user_id)
        
        print("RECOVERY PLAN:")
        for i, action in enumerate(setback.recovery_actions, 1):
            print(f"  {i}. {action}")
        print()
        print("REASONING FOR RECOVERY PLAN:")
        for i, reason in enumerate(recovery_decision.reasoning, 1):
            print(f"  {i}. {reason}")
        print()
    
    # Feature 6: Decision History (Transparency)
    print("🔍 Feature 6: Complete Decision History")
    print("-" * 70)
    
    all_decisions = store.load_decisions(user_id)
    print(f"✓ Total decisions recorded: {len(all_decisions)}")
    print()
    print("Recent decisions:")
    for i, dec in enumerate(all_decisions[-3:], 1):
        print(f"  {i}. [{dec.decision_type}] {dec.timestamp.strftime('%Y-%m-%d %H:%M')}")
        print(f"     Confidence: {dec.confidence*100:.0f}%")
    print()
    
    # Summary
    print("=" * 70)
    print("Summary: Key Features Demonstrated")
    print("=" * 70)
    print("✓ Goal creation with milestones and deadlines")
    print("✓ Progress tracking with sentiment analysis")
    print("✓ Behavior adaptation based on user patterns")
    print("✓ AI coaching with transparent reasoning")
    print("✓ Automatic setback detection")
    print("✓ Personalized recovery plans")
    print("✓ Complete decision history for transparency")
    print()
    print("All features are designed to:")
    print("  • Adapt to real human behavior")
    print("  • Recover from setbacks proactively")
    print("  • Provide transparent reasoning for all decisions")
    print()


if __name__ == "__main__":
    demonstrate_nia()
