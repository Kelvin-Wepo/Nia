# Nia - AI Goal Coaching Platform

An agentic AI goal coaching platform that helps users achieve goals by adapting to real human behavior, recovering from setbacks, and providing transparent reasoning for all decisions.

## Features

### 🤖 Agentic AI Coaching
- Intelligent AI agent that provides personalized coaching advice
- Proactive guidance based on your goals and progress
- Context-aware recommendations

### 🎯 Behavior Adaptation
- Learns from your interaction patterns
- Adapts coaching style to your preferences
- Tracks motivation levels and engagement patterns
- Personalizes advice based on your behavior profile

### 🔄 Setback Recovery
- Automatically detects setbacks:
  - Missed milestones
  - Loss of motivation
  - External obstacles
  - Negative sentiment patterns
- Generates personalized recovery plans
- Provides actionable steps to get back on track

### 🔍 Transparent Reasoning
- Every decision includes detailed reasoning
- See exactly why the AI coach recommends specific actions
- View factors considered in each decision
- Access complete decision history for full transparency

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kelvin-Wepo/Nia.git
cd Nia
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Configure OpenAI API for advanced AI features:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

**Note:** Nia works with or without an OpenAI API key. Without the API key, it uses a built-in mock AI that still provides intelligent coaching based on rules and patterns.

## Quick Start

Run the interactive CLI:
```bash
python nia_cli.py
```

### Basic Workflow

1. **Create a Goal**
   - Set a title and description
   - Define milestones
   - Set target dates (optional)

2. **Update Progress**
   - Log your progress regularly
   - Mark milestones as completed
   - Share how you're feeling

3. **Get Coaching Advice**
   - Request personalized advice anytime
   - View transparent reasoning behind suggestions
   - See what factors influenced the advice

4. **Handle Setbacks**
   - Nia automatically detects setbacks
   - Get recovery plans with specific actions
   - Understand why setbacks were detected

## Architecture

### Core Components

1. **Models (`models.py`)**
   - Domain models for goals, progress, setbacks, and decisions
   - User behavior profiles for adaptation
   - Transparent decision tracking

2. **Agent (`agent.py`)**
   - `NiaCoachingAgent`: Main AI coaching logic
   - Setback detection algorithms
   - Recovery plan generation
   - Behavior-adaptive advice generation

3. **Storage (`storage.py`)**
   - JSON-based data persistence
   - User data management
   - Decision history tracking

4. **CLI (`nia_cli.py`)**
   - Interactive command-line interface
   - User-friendly goal management
   - Transparent decision viewing

## Key Features in Detail

### Behavior Adaptation

Nia tracks and adapts to:
- Preferred check-in times
- Average progress rates
- Typical setback recovery patterns
- Motivation levels
- Response to different coaching styles
- Engagement patterns

Example:
```python
# Nia learns that you prefer encouragement when motivation is low
if user.motivation_level < 0.4 and user.response_to_encouragement == "positive":
    advice = "Focus on small wins to rebuild momentum"
```

### Setback Detection

Nia automatically detects:
1. **Missed Milestones**: Target dates passed without completion
2. **Loss of Motivation**: Extended periods without updates
3. **External Obstacles**: Patterns of negative sentiment
4. **Skill Gaps**: Identified through progress descriptions
5. **Time Constraints**: Timeline analysis

### Transparent Reasoning

Every decision includes:
- Step-by-step reasoning
- Factors considered (motivation, progress rate, etc.)
- Confidence level
- Decision type and context

Example transparency report:
```
Decision: Focus on completing the first milestone

Reasoning:
1. Current completion rate: 0%
2. User engagement pattern: consistent
3. User motivation level: 0.50
4. Adapting tone for lower motivation - focusing on encouragement

Confidence: 80%

Factors Considered:
  - goal_status: active
  - milestones_completed: 0
  - motivation_level: 0.5
```

## Running Tests

```bash
pytest test_nia.py -v
```

Tests cover:
- Model creation and validation
- Setback detection logic
- Recovery plan generation
- Behavior adaptation
- Data persistence
- Transparency features

## Example Usage

### Python API

```python
from models import Goal
from agent import NiaCoachingAgent
from storage import DataStore

# Initialize
agent = NiaCoachingAgent(user_id="user123", use_mock=True)
store = DataStore()

# Create a goal
goal = Goal(
    id="goal-1",
    title="Learn Machine Learning",
    description="Complete ML course and build a project",
    milestones=["Finish course", "Build project", "Deploy model"]
)

store.save_goal(goal, "user123")

# Get coaching advice
recent_updates = store.load_progress("user123", goal.id, limit=10)
decision = agent.generate_coaching_advice(goal, recent_updates)

print(decision.decision)
print("\nReasoning:")
for reason in decision.reasoning:
    print(f"- {reason}")

# Check for setbacks
setback = agent.detect_setback(goal, recent_updates)
if setback:
    recovery = agent.create_recovery_plan(setback, goal)
    print(f"\nRecovery actions:")
    for action in setback.recovery_actions:
        print(f"- {action}")
```

## Data Storage

Data is stored in JSON files under `user_data/`:
```
user_data/
├── user123/
│   ├── goals.json
│   ├── progress_goal-1.json
│   ├── setbacks_goal-1.json
│   ├── behavior_profile.json
│   └── decisions.json
```

## Configuration

Environment variables (optional):
- `OPENAI_API_KEY`: OpenAI API key for advanced AI features
- `NIA_USER_ID`: Default user ID (defaults to "default_user")

## Design Principles

1. **Transparency First**: Every decision is explainable
2. **Adaptive by Default**: Learns from user behavior automatically
3. **Resilience Focused**: Proactively handles setbacks
4. **Privacy Conscious**: All data stored locally
5. **Minimal Dependencies**: Works with or without external APIs

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional setback detection patterns
- More sophisticated behavior adaptation
- Natural language processing for progress updates
- Integration with external tools (calendars, task managers)
- Web or mobile interface

## License

MIT License - feel free to use and modify as needed.

## Acknowledgments

Nia is designed to be a supportive, transparent, and adaptive AI coach that truly understands human behavior and helps users achieve their goals through difficult times.