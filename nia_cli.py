"""
Command-line interface for Nia AI Goal Coaching Platform.
"""
import sys
import os
from datetime import datetime, timedelta
from typing import Optional
import uuid

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from models import Goal, ProgressUpdate, GoalStatus, SetbackType
from agent import NiaCoachingAgent
from storage import DataStore


class NiaCLI:
    """Command-line interface for interacting with Nia."""
    
    def __init__(self, user_id: str = "default_user"):
        """Initialize the CLI."""
        self.user_id = user_id
        self.store = DataStore()
        self.agent = NiaCoachingAgent(user_id=user_id, use_mock=True)
        
        # Load existing behavior profile if available
        profile = self.store.load_behavior_profile(user_id)
        if profile:
            self.agent.behavior_profile = profile
    
    def run(self):
        """Run the interactive CLI."""
        print("=" * 60)
        print("Welcome to Nia - Your AI Goal Coaching Platform")
        print("=" * 60)
        print()
        print("Nia adapts to your behavior, helps you recover from setbacks,")
        print("and provides transparent reasoning for all advice.")
        print()
        
        while True:
            print("\nMain Menu:")
            print("1. Create a new goal")
            print("2. View my goals")
            print("3. Update progress on a goal")
            print("4. Get coaching advice")
            print("5. Check for setbacks")
            print("6. View decision history (transparency)")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                self.create_goal()
            elif choice == "2":
                self.view_goals()
            elif choice == "3":
                self.update_progress()
            elif choice == "4":
                self.get_advice()
            elif choice == "5":
                self.check_setbacks()
            elif choice == "6":
                self.view_decision_history()
            elif choice == "7":
                print("\nThank you for using Nia! Keep working towards your goals!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def create_goal(self):
        """Create a new goal interactively."""
        print("\n" + "=" * 60)
        print("Create a New Goal")
        print("=" * 60)
        
        title = input("Goal title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        
        description = input("Goal description: ").strip()
        
        days_str = input("Target days from now (press Enter to skip): ").strip()
        target_date = None
        if days_str and days_str.isdigit():
            target_date = datetime.now() + timedelta(days=int(days_str))
        
        milestones_input = input("Enter milestones (comma-separated, or press Enter to skip): ").strip()
        milestones = [m.strip() for m in milestones_input.split(",")] if milestones_input else []
        
        goal = Goal(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            target_date=target_date,
            milestones=milestones
        )
        
        self.store.save_goal(goal, self.user_id)
        
        print(f"\n✓ Goal created successfully! ID: {goal.id}")
        print(f"  Title: {goal.title}")
        if goal.target_date:
            print(f"  Target date: {goal.target_date.strftime('%Y-%m-%d')}")
        if goal.milestones:
            print(f"  Milestones: {len(goal.milestones)}")
    
    def view_goals(self):
        """View all goals."""
        print("\n" + "=" * 60)
        print("Your Goals")
        print("=" * 60)
        
        goals = self.store.load_goals(self.user_id)
        
        if not goals:
            print("No goals found. Create your first goal!")
            return
        
        for i, goal in enumerate(goals, 1):
            print(f"\n{i}. {goal.title} [{goal.status.value}]")
            print(f"   ID: {goal.id}")
            print(f"   {goal.description}")
            
            if goal.target_date:
                days_remaining = (goal.target_date - datetime.now()).days
                print(f"   Target: {goal.target_date.strftime('%Y-%m-%d')} ({days_remaining} days remaining)")
            
            if goal.milestones:
                completion = len(goal.completed_milestones) / len(goal.milestones) * 100
                print(f"   Progress: {len(goal.completed_milestones)}/{len(goal.milestones)} milestones ({completion:.0f}%)")
    
    def update_progress(self):
        """Update progress on a goal."""
        goals = self.store.load_goals(self.user_id)
        
        if not goals:
            print("\nNo goals found. Create a goal first!")
            return
        
        print("\n" + "=" * 60)
        print("Update Progress")
        print("=" * 60)
        
        # Show active goals
        active_goals = [g for g in goals if g.status == GoalStatus.ACTIVE]
        if not active_goals:
            print("No active goals.")
            return
        
        for i, goal in enumerate(active_goals, 1):
            print(f"{i}. {goal.title}")
        
        choice = input("\nSelect a goal (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(active_goals):
            print("Invalid choice.")
            return
        
        goal = active_goals[int(choice) - 1]
        
        print(f"\nUpdating: {goal.title}")
        progress_desc = input("Describe your progress: ").strip()
        
        if not progress_desc:
            print("Progress description cannot be empty.")
            return
        
        # Check if milestone completed
        milestone_completed = None
        if goal.milestones:
            incomplete = [m for m in goal.milestones if m not in goal.completed_milestones]
            if incomplete:
                print("\nDid you complete a milestone?")
                for i, m in enumerate(incomplete, 1):
                    print(f"{i}. {m}")
                print(f"{len(incomplete) + 1}. No milestone completed")
                
                milestone_choice = input("Select (number): ").strip()
                if milestone_choice.isdigit():
                    idx = int(milestone_choice) - 1
                    if 0 <= idx < len(incomplete):
                        milestone_completed = incomplete[idx]
                        goal.completed_milestones.append(milestone_completed)
                        self.store.save_goal(goal, self.user_id)
        
        sentiment = input("How do you feel about this progress? (positive/neutral/negative): ").strip().lower()
        if sentiment not in ["positive", "neutral", "negative"]:
            sentiment = "neutral"
        
        progress = ProgressUpdate(
            goal_id=goal.id,
            progress_description=progress_desc,
            milestone_completed=milestone_completed,
            sentiment=sentiment
        )
        
        self.store.save_progress(progress, self.user_id)
        
        # Update behavior profile
        motivation_map = {"positive": 0.8, "neutral": 0.5, "negative": 0.3}
        self.agent.update_behavior_profile({
            "check_in_hour": datetime.now().hour,
            "motivation_indicator": motivation_map[sentiment]
        })
        self.store.save_behavior_profile(self.agent.behavior_profile)
        
        print("\n✓ Progress updated successfully!")
        if milestone_completed:
            print(f"  🎉 Milestone completed: {milestone_completed}")
    
    def get_advice(self):
        """Get coaching advice for a goal."""
        goals = self.store.load_goals(self.user_id)
        
        if not goals:
            print("\nNo goals found. Create a goal first!")
            return
        
        print("\n" + "=" * 60)
        print("Get Coaching Advice")
        print("=" * 60)
        
        active_goals = [g for g in goals if g.status == GoalStatus.ACTIVE]
        if not active_goals:
            print("No active goals.")
            return
        
        for i, goal in enumerate(active_goals, 1):
            print(f"{i}. {goal.title}")
        
        choice = input("\nSelect a goal (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(active_goals):
            print("Invalid choice.")
            return
        
        goal = active_goals[int(choice) - 1]
        recent_updates = self.store.load_progress(self.user_id, goal.id, limit=10)
        
        print(f"\nGenerating advice for: {goal.title}")
        print("(This uses transparent AI reasoning...)\n")
        
        decision = self.agent.generate_coaching_advice(goal, recent_updates)
        self.store.save_decision(decision, self.user_id)
        
        print("=" * 60)
        print("ADVICE")
        print("=" * 60)
        print(decision.decision)
        print()
        
        show_reasoning = input("Show transparent reasoning? (y/n): ").strip().lower()
        if show_reasoning == 'y':
            print("\n" + "=" * 60)
            print("TRANSPARENT REASONING")
            print("=" * 60)
            print(self.agent.get_transparency_report(decision))
    
    def check_setbacks(self):
        """Check for setbacks in goals."""
        goals = self.store.load_goals(self.user_id)
        
        if not goals:
            print("\nNo goals found.")
            return
        
        print("\n" + "=" * 60)
        print("Checking for Setbacks")
        print("=" * 60)
        
        found_setbacks = False
        
        for goal in goals:
            if goal.status != GoalStatus.ACTIVE:
                continue
            
            recent_updates = self.store.load_progress(self.user_id, goal.id, limit=10)
            setback = self.agent.detect_setback(goal, recent_updates)
            
            if setback:
                found_setbacks = True
                print(f"\n⚠ Setback detected for: {goal.title}")
                print(f"   Type: {setback.type.value}")
                print(f"   Description: {setback.description}")
                
                # Generate recovery plan
                print("\n   Generating recovery plan...")
                decision = self.agent.create_recovery_plan(setback, goal)
                self.store.save_decision(decision, self.user_id)
                self.store.save_setback(setback, self.user_id)
                
                print("\n   RECOVERY PLAN:")
                for i, action in enumerate(setback.recovery_actions, 1):
                    print(f"   {i}. {action}")
                
                show_reasoning = input("\n   Show transparent reasoning? (y/n): ").strip().lower()
                if show_reasoning == 'y':
                    print("\n" + "-" * 60)
                    print(self.agent.get_transparency_report(decision))
        
        if not found_setbacks:
            print("\n✓ No setbacks detected. Keep up the great work!")
    
    def view_decision_history(self):
        """View decision history for transparency."""
        print("\n" + "=" * 60)
        print("Decision History (Transparency)")
        print("=" * 60)
        
        decisions = self.store.load_decisions(self.user_id, limit=10)
        
        if not decisions:
            print("No decisions recorded yet.")
            return
        
        print(f"\nShowing last {len(decisions)} decisions:\n")
        
        for i, decision in enumerate(reversed(decisions), 1):
            print(f"{i}. [{decision.decision_type}] {decision.timestamp.strftime('%Y-%m-%d %H:%M')}")
            print(f"   {decision.decision[:80]}...")
            print(f"   Confidence: {decision.confidence*100:.0f}%")
            
            if i < len(decisions):
                print()
        
        view_detail = input("\nView detailed reasoning for a decision? (enter number or 'n'): ").strip()
        if view_detail.isdigit():
            idx = int(view_detail) - 1
            if 0 <= idx < len(decisions):
                decision = list(reversed(decisions))[idx]
                print("\n" + "=" * 60)
                print(self.agent.get_transparency_report(decision))


def main():
    """Main entry point for the CLI."""
    user_id = os.getenv("NIA_USER_ID", "default_user")
    
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    
    cli = NiaCLI(user_id=user_id)
    
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
