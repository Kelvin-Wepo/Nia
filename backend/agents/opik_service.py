"""
Opik Integration for Agent Observability

This module integrates the Opik SDK for tracking and evaluating agent decisions.
"""

from typing import Dict, Any, Optional
import time
from functools import wraps

try:
    from opik import Opik
    from opik.decorators import track
    OPIK_AVAILABLE = True
except ImportError:
    OPIK_AVAILABLE = False
    print("Warning: Opik SDK not available. Install with: pip install opik")


class OpikService:
    """Service for tracking agent decisions with Opik"""
    
    def __init__(self):
        if OPIK_AVAILABLE:
            self.client = Opik()
        else:
            self.client = None
    
    def track_decision(
        self,
        decision_type: str,
        context: Dict[str, Any],
        decision: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Track an agent decision with Opik.
        
        Args:
            decision_type: Type of decision being made
            context: Input context for the decision
            decision: The decision output
            metadata: Additional metadata
        
        Returns:
            Dict containing trace_id and span_id
        """
        if not self.client:
            return {'trace_id': '', 'span_id': ''}
        
        try:
            trace = self.client.trace(
                name=f"agent_decision_{decision_type}",
                input=context,
                output=decision,
                metadata=metadata or {}
            )
            
            return {
                'trace_id': trace.id,
                'span_id': trace.id
            }
        except Exception as e:
            print(f"Error tracking with Opik: {e}")
            return {'trace_id': '', 'span_id': ''}
    
    def log_performance_metric(
        self,
        decision_id: str,
        metric_name: str,
        metric_value: float,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a performance metric for a decision.
        
        Args:
            decision_id: ID of the decision
            metric_name: Name of the metric
            metric_value: Value of the metric
            metadata: Additional metadata
        """
        if not self.client:
            return
        
        try:
            self.client.log_metric(
                name=metric_name,
                value=metric_value,
                trace_id=decision_id,
                metadata=metadata or {}
            )
        except Exception as e:
            print(f"Error logging metric: {e}")
    
    def track_experiment(
        self,
        experiment_name: str,
        variant: str,
        outcome: Dict[str, Any]
    ):
        """
        Track an A/B experiment outcome.
        
        Args:
            experiment_name: Name of the experiment
            variant: Which variant was used
            outcome: Outcome data
        """
        if not self.client:
            return
        
        try:
            self.client.log_experiment(
                name=experiment_name,
                variant=variant,
                outcome=outcome
            )
        except Exception as e:
            print(f"Error tracking experiment: {e}")


def track_agent_decision(decision_type: str):
    """
    Decorator to track agent decisions with Opik.
    
    Usage:
        @track_agent_decision('strategy_selection')
        def select_strategy(context):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Extract context from args/kwargs
            context = kwargs.get('context', {})
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Calculate duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Track with Opik
            opik_service = OpikService()
            tracking_info = opik_service.track_decision(
                decision_type=decision_type,
                context=context,
                decision=result,
                metadata={'duration_ms': duration_ms}
            )
            
            # Add tracking info to result if it's a dict
            if isinstance(result, dict):
                result['opik_trace_id'] = tracking_info['trace_id']
                result['opik_span_id'] = tracking_info['span_id']
            
            return result
        
        return wrapper
    return decorator


# Example usage functions
def evaluate_agent_performance(agent_decisions: list) -> Dict[str, Any]:
    """
    Evaluate overall agent performance using Opik.
    
    Args:
        agent_decisions: List of agent decision records
    
    Returns:
        Dict containing evaluation metrics
    """
    if not OPIK_AVAILABLE:
        return {'error': 'Opik not available'}
    
    # Calculate metrics
    total_decisions = len(agent_decisions)
    successful = sum(1 for d in agent_decisions if d.get('was_helpful', False))
    avg_confidence = sum(d.get('confidence_score', 0) for d in agent_decisions) / total_decisions if total_decisions > 0 else 0
    
    return {
        'total_decisions': total_decisions,
        'success_rate': successful / total_decisions if total_decisions > 0 else 0,
        'average_confidence': avg_confidence,
        'timestamp': time.time()
    }
