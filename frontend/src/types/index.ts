export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  bio?: string
  timezone: string
  coaching_style_preference: 'supportive' | 'direct' | 'analytical' | 'motivational'
  preferred_check_in_frequency: 'daily' | 'weekly' | 'biweekly'
  created_at: string
  last_active: string
}

export interface Goal {
  id: number
  user: number
  title: string
  description: string
  category: string
  tags: string[]
  status: 'active' | 'paused' | 'completed' | 'abandoned'
  priority: 'low' | 'medium' | 'high' | 'critical'
  start_date: string
  target_date: string
  completed_date?: string
  progress_percentage: number
  is_on_track: boolean
  predicted_completion_date?: string
  risk_factors: string[]
  success_likelihood: number
  current_strategy: Record<string, any>
  strategy_adjustments_count: number
  created_at: string
  updated_at: string
}

export interface Milestone {
  id: number
  goal: number
  title: string
  description: string
  target_date: string
  completed_date?: string
  is_completed: boolean
  order: number
  created_at: string
  updated_at: string
}

export interface ProgressUpdate {
  id: number
  goal: number
  update_text: string
  progress_percentage: number
  mood: 'motivated' | 'neutral' | 'struggling' | 'frustrated' | 'confident'
  attachments: any[]
  sentiment_score?: number
  key_insights: string[]
  created_at: string
}

export interface Setback {
  id: number
  goal: number
  description: string
  severity: 'minor' | 'moderate' | 'major' | 'critical'
  setback_type: string
  root_causes: string[]
  is_resolved: boolean
  resolution_strategy: string
  recovery_actions: any[]
  ai_recovery_plan: Record<string, any>
  similar_past_setbacks: any[]
  occurred_at: string
  resolved_at?: string
}

export interface CoachingSession {
  id: number
  user: number
  goal?: number
  session_type: 'check_in' | 'goal_setting' | 'setback_recovery' | 'strategy_adjustment' | 'celebration' | 'reflection'
  title: string
  context: Record<string, any>
  user_state: Record<string, any>
  outcome_summary: string
  action_items: any[]
  insights_gained: string[]
  agent_confidence: number
  reasoning_chain: any[]
  started_at: string
  completed_at?: string
  duration_minutes: number
}

export interface Message {
  id: number
  session: number
  role: 'user' | 'assistant' | 'system'
  content: string
  metadata: Record<string, any>
  reasoning: string
  confidence_score?: number
  timestamp: string
}

export interface Intervention {
  id: number
  user: number
  goal: number
  intervention_type: 'motivational' | 'corrective' | 'supportive' | 'challenging' | 'informational'
  trigger_reason: string
  message: string
  recommended_actions: any[]
  decision_reasoning: string
  confidence_level: number
  alternative_approaches: any[]
  was_helpful?: boolean
  user_feedback: string
  outcome: string
  created_at: string
}

export interface AgentDecision {
  id: number
  user: number
  goal?: number
  decision_type: 'strategy_selection' | 'intervention_trigger' | 'goal_adjustment' | 'milestone_suggestion' | 'recovery_plan' | 'encouragement'
  context: Record<string, any>
  user_state: Record<string, any>
  decision: string
  rationale: string
  reasoning_steps: any[]
  alternatives_considered: any[]
  confidence_score: number
  risk_assessment: Record<string, any>
  model_name: string
  model_version: string
  opik_trace_id: string
  opik_span_id: string
  created_at: string
}

export interface LearningRecord {
  id: number
  user: number
  insight_type: string
  insight_description: string
  supporting_data: Record<string, any>
  confidence: number
  applied_to_decisions: number
  success_rate: number
  is_validated: boolean
  validation_method: string
  created_at: string
  updated_at: string
}
