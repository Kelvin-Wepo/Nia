"""
Python API Usage Examples for Nia AI Goal Coaching Platform.

This file demonstrates how to use Nia programmatically in your own applications.
"""
import uuid
from datetime import datetime, timedelta

from models import Goal, ProgressUpdate, GoalStatus
from agent import NiaCoachingAgent
from storage import DataStore


# Example 1: Basic Setup
print("=" * 70)
print("Example 1: Basic Setup")
print("=" * 70)

# Initialize components
user_id = "example_user"
agent = NiaCoachingAgent(user_id=user_id, use_mock=True)
store = DataStore(data_dir="example_data")

print(f"✓ Agent initialized for user: {user_id}")
print(f"✓ Using mock AI: {agent.use_mock}")
print()


# Example 2: Creating and Managing Goals
print("=" * 70)
print("Example 2: Creating and Managing Goals")
print("=" * 70)

# Create a goal with milestones
goal = Goal(
    id=str(uuid.uuid4()),
    title="Learn Data Science",
    description="Become proficient in data science and machine learning",
    target_date=datetime.now() + timedelta(days=180),
    milestones=[
        "Complete Python basics",
        "Learn NumPy and Pandas",
        "Study statistics and probability",
        "Master machine learning algorithms",
        "Build portfolio projects"
    ]
)

# Save the goal
store.save_goal(goal, user_id)
print(f"✓ Created goal: {goal.title}")
print(f"  ID: {goal.id}")
print(f"  Milestones: {len(goal.milestones)}")
print()


# Example 3: Recording Progress
print("=" * 70)
print("Example 3: Recording Progress")
print("=" * 70)

# Record progress update
progress = ProgressUpdate(
    goal_id=goal.id,
    progress_description="Completed Python basics course on Coursera",
    milestone_completed="Complete Python basics",
    sentiment="positive"
)

store.save_progress(progress, user_id)

# Update goal to reflect completed milestone
goal.completed_milestones.append("Complete Python basics")
store.save_goal(goal, user_id)

print(f"✓ Progress recorded")
print(f"  Milestone completed: {progress.milestone_completed}")
print(f"  Progress: {len(goal.completed_milestones)}/{len(goal.milestones)} milestones")
print()

# Update behavior profile based on interaction
agent.update_behavior_profile({
    "check_in_hour": datetime.now().hour,
    "motivation_indicator": 0.8  # High motivation
})
store.save_behavior_profile(agent.behavior_profile)

print(f"✓ Behavior profile updated")
print(f"  Motivation level: {agent.behavior_profile.motivation_level:.2f}")
print()


# Example 4: Getting Coaching Advice
print("=" * 70)
print("Example 4: Getting Coaching Advice")
print("=" * 70)

# Load recent progress
recent_updates = store.load_progress(user_id, goal.id, limit=10)

# Get personalized coaching advice
decision = agent.generate_coaching_advice(goal, recent_updates)
store.save_decision(decision, user_id)

print("Coaching Advice:")
print(f"  {decision.decision}")
print()

print("Transparent Reasoning:")
for i, reason in enumerate(decision.reasoning, 1):
    print(f"  {i}. {reason}")
print()


# Example 5: Detecting and Recovering from Setbacks
print("=" * 70)
print("Example 5: Detecting and Recovering from Setbacks")
print("=" * 70)

# Simulate a setback scenario with negative updates
setback_updates = [
    ProgressUpdate(
        goal_id=goal.id,
        progress_description="Feeling stuck on NumPy concepts",
        sentiment="negative",
        timestamp=datetime.now() - timedelta(days=2)
    ),
    ProgressUpdate(
        goal_id=goal.id,
        progress_description="Still struggling, losing motivation",
        sentiment="negative",
        timestamp=datetime.now() - timedelta(days=1)
    ),
    ProgressUpdate(
        goal_id=goal.id,
        progress_description="Not making progress this week",
        sentiment="negative",
        timestamp=datetime.now()
    )
]

for update in setback_updates:
    store.save_progress(update, user_id)

# Check for setbacks
all_updates = store.load_progress(user_id, goal.id)
setback = agent.detect_setback(goal, all_updates)

if setback:
    print(f"⚠ Setback Detected:")
    print(f"  Type: {setback.type.value}")
    print(f"  Description: {setback.description}")
    print()
    
    # Generate recovery plan
    recovery_decision = agent.create_recovery_plan(setback, goal)
    store.save_setback(setback, user_id)
    store.save_decision(recovery_decision, user_id)
    
    print("Recovery Plan:")
    for i, action in enumerate(setback.recovery_actions, 1):
        print(f"  {i}. {action}")
    print()


# Example 6: Viewing Transparency Reports
print("=" * 70)
print("Example 6: Viewing Transparency Reports")
print("=" * 70)

# Get the most recent decision
recent_decisions = store.load_decisions(user_id, limit=1)
if recent_decisions:
    latest_decision = recent_decisions[0]
    
    print("Latest Decision Transparency Report:")
    print("-" * 70)
    print(agent.get_transparency_report(latest_decision))


# Example 7: Accessing Behavior Profile
print("=" * 70)
print("Example 7: Accessing Behavior Profile")
print("=" * 70)

profile = store.load_behavior_profile(user_id)
if profile:
    print("User Behavior Profile:")
    print(f"  Motivation Level: {profile.motivation_level:.2f}")
    print(f"  Engagement Pattern: {profile.engagement_pattern}")
    print(f"  Response to Encouragement: {profile.response_to_encouragement}")
    print(f"  Typical Recovery Time: {profile.typical_setback_recovery_days} days")
    if profile.preferred_check_in_times:
        avg_hour = sum(profile.preferred_check_in_times) / len(profile.preferred_check_in_times)
        print(f"  Preferred Check-in Time: ~{avg_hour:.0f}:00")
    print()


# Example 8: Goal Status Management
print("=" * 70)
print("Example 8: Goal Status Management")
print("=" * 70)

# Load all goals
all_goals = store.load_goals(user_id)
print(f"Total goals: {len(all_goals)}")
print()

for goal in all_goals:
    completion_rate = 0
    if goal.milestones:
        completion_rate = len(goal.completed_milestones) / len(goal.milestones) * 100
    
    print(f"  • {goal.title}")
    print(f"    Status: {goal.status.value}")
    print(f"    Progress: {completion_rate:.0f}%")
    
    if goal.target_date:
        days_remaining = (goal.target_date - datetime.now()).days
        print(f"    Days remaining: {days_remaining}")
    print()


# Example 9: Integration Pattern for Custom Applications
print("=" * 70)
print("Example 9: Integration Pattern for Custom Applications")
print("=" * 70)

print("""
Integration Pattern:

1. Initialize once per user session:
   agent = NiaCoachingAgent(user_id=user_id, use_mock=True)
   store = DataStore()

2. On user action (create goal, log progress):
   - Create/update domain objects (Goal, ProgressUpdate)
   - Save to store
   - Update behavior profile

3. Proactive coaching (scheduled or triggered):
   - Load recent data: goals, updates
   - Check for setbacks: agent.detect_setback()
   - Generate advice: agent.generate_coaching_advice()
   - Save decisions for transparency

4. User requests help:
   - Load context (goal, progress history)
   - Generate personalized advice
   - Show transparent reasoning

5. Periodic review:
   - Analyze behavior patterns
   - Adjust coaching strategies
   - Update user profile
""")


print("=" * 70)
print("Examples Complete!")
print("=" * 70)
print()
print("Key Takeaways:")
print("  • All AI decisions include transparent reasoning")
print("  • System adapts to user behavior automatically")
print("  • Setback detection and recovery is proactive")
print("  • Everything is stored locally for privacy")
print("  • Works with or without OpenAI API")
print()
