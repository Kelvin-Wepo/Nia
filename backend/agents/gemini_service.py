"""
Gemini AI Service for Nia Coaching Platform

This module integrates Google's Gemini AI for intelligent coaching decisions.
"""

import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Any
import json


class GeminiService:
    """Service for interacting with Google's Gemini AI"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def generate_coaching_response(
        self, 
        user_message: str, 
        context: Dict[str, Any],
        coaching_style: str = 'supportive'
    ) -> Dict[str, Any]:
        """
        Generate a coaching response based on user message and context.
        
        Args:
            user_message: The user's message
            context: Context including user state, goal progress, history
            coaching_style: The coaching style preference
        
        Returns:
            Dict containing response, reasoning, and confidence
        """
        prompt = self._build_coaching_prompt(user_message, context, coaching_style)
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                'response': response.text,
                'reasoning': self._extract_reasoning(response),
                'confidence': self._calculate_confidence(response),
                'model': settings.GEMINI_MODEL
            }
        except Exception as e:
            return {
                'response': "I'm having trouble processing that right now. Let's try again.",
                'reasoning': f"Error: {str(e)}",
                'confidence': 0.0,
                'model': settings.GEMINI_MODEL
            }
    
    def analyze_setback(
        self, 
        setback_description: str, 
        user_history: Dict[str, Any],
        goal_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a setback and provide recovery strategies.
        
        Args:
            setback_description: Description of the setback
            user_history: User's behavioral history
            goal_context: Context about the goal
        
        Returns:
            Dict containing analysis, recovery plan, and reasoning
        """
        prompt = f"""
        As an empathetic AI coach, analyze this setback and create a recovery plan.
        
        Setback: {setback_description}
        
        User History:
        - Past setback patterns: {user_history.get('typical_setback_patterns', {})}
        - Success triggers: {user_history.get('success_triggers', {})}
        
        Goal Context:
        - Goal: {goal_context.get('title')}
        - Current progress: {goal_context.get('progress_percentage')}%
        - Priority: {goal_context.get('priority')}
        
        Provide:
        1. Root cause analysis
        2. Emotional validation
        3. Concrete recovery steps
        4. Similar past situations and outcomes
        5. Adjusted timeline if needed
        
        Format your response as JSON with keys: analysis, recovery_plan, timeline_adjustment, reasoning
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            result['confidence'] = self._calculate_confidence(response)
            return result
        except Exception as e:
            return {
                'analysis': 'Unable to analyze setback',
                'recovery_plan': [],
                'timeline_adjustment': None,
                'reasoning': f'Error: {str(e)}',
                'confidence': 0.0
            }
    
    def suggest_strategy_adjustment(
        self,
        goal: Dict[str, Any],
        recent_progress: List[Dict[str, Any]],
        user_behavior: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Suggest adjustments to coaching strategy based on progress.
        
        Args:
            goal: Goal information
            recent_progress: Recent progress updates
            user_behavior: User behavioral patterns
        
        Returns:
            Dict containing suggested adjustments and reasoning
        """
        prompt = f"""
        As an adaptive AI coach, analyze this goal's progress and suggest strategy adjustments.
        
        Goal: {goal.get('title')}
        Current Strategy: {goal.get('current_strategy')}
        Recent Progress: {json.dumps(recent_progress, indent=2)}
        User Behavior Patterns: {json.dumps(user_behavior, indent=2)}
        
        Determine if the current strategy is working or if adjustments are needed.
        Consider:
        1. Progress velocity
        2. User engagement patterns
        3. Mood trends
        4. Setback frequency
        
        Provide strategy adjustment recommendations with clear reasoning.
        Format as JSON with keys: should_adjust, new_strategy, reasoning, expected_impact
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            result['confidence'] = self._calculate_confidence(response)
            return result
        except Exception as e:
            return {
                'should_adjust': False,
                'new_strategy': {},
                'reasoning': f'Error: {str(e)}',
                'expected_impact': 'Unknown',
                'confidence': 0.0
            }
    
    def generate_intervention(
        self,
        trigger: str,
        user_state: Dict[str, Any],
        goal_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a coaching intervention based on triggers.
        
        Args:
            trigger: What triggered the intervention
            user_state: Current user state (mood, energy, etc.)
            goal_state: Current goal state
        
        Returns:
            Dict containing intervention details and reasoning
        """
        prompt = f"""
        As a proactive AI coach, create an intervention for this situation.
        
        Trigger: {trigger}
        User State: {json.dumps(user_state, indent=2)}
        Goal State: {json.dumps(goal_state, indent=2)}
        
        Create an appropriate intervention that:
        1. Addresses the trigger
        2. Considers user's current state
        3. Provides actionable guidance
        4. Maintains motivation
        
        Format as JSON with keys: intervention_type, message, recommended_actions, reasoning
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            result['confidence'] = self._calculate_confidence(response)
            return result
        except Exception as e:
            return {
                'intervention_type': 'supportive',
                'message': 'Stay focused on your goals!',
                'recommended_actions': [],
                'reasoning': f'Error: {str(e)}',
                'confidence': 0.0
            }
    
    def _build_coaching_prompt(
        self, 
        user_message: str, 
        context: Dict[str, Any],
        coaching_style: str
    ) -> str:
        """Build a comprehensive prompt for coaching responses"""
        return f"""
        You are Nia, an empathetic and adaptive AI goal coach. Your role is to help users 
        achieve their goals by understanding human behavior, recovering from setbacks, and 
        providing transparent reasoning for your guidance.
        
        Coaching Style: {coaching_style}
        
        User Message: {user_message}
        
        Context:
        - User goals: {context.get('goals', [])}
        - Current progress: {context.get('progress', {})}
        - Recent mood: {context.get('mood', 'neutral')}
        - Behavioral patterns: {context.get('patterns', {})}
        
        Respond with:
        1. An empathetic, personalized coaching response
        2. Specific, actionable guidance
        3. Encouragement that acknowledges their efforts
        
        Be conversational, supportive, and practical. Show your reasoning when making suggestions.
        """
    
    def _extract_reasoning(self, response) -> str:
        """Extract reasoning from the AI response"""
        # This is a simplified version - in production, you'd parse structured output
        return "Reasoning based on user context and coaching best practices"
    
    def _calculate_confidence(self, response) -> float:
        """Calculate confidence score for the response"""
        # This is a simplified version - in production, you'd use actual model confidence
        return 0.85
