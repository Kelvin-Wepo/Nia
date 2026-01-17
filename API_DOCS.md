# Nia API Documentation

## Authentication

All API endpoints (except registration and login) require JWT authentication.

### Obtaining Tokens

**POST** `/api/token/`

Request:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Tokens

Include the access token in the Authorization header:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refreshing Tokens

**POST** `/api/token/refresh/`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## User Management

### Register New User

**POST** `/api/users/register/`

Request:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "coaching_style_preference": "supportive",
  "preferred_check_in_frequency": "weekly"
}
```

### Get Current User

**GET** `/api/users/me/`

Response:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "coaching_style_preference": "supportive",
  "preferred_check_in_frequency": "weekly",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Goals

### List Goals

**GET** `/api/goals/goals/`

Query Parameters:
- `status`: Filter by status (active, paused, completed, abandoned)
- `priority`: Filter by priority (low, medium, high, critical)
- `category`: Filter by category

### Create Goal

**POST** `/api/goals/goals/`

Request:
```json
{
  "title": "Learn Python",
  "description": "Master Python programming in 3 months",
  "category": "Learning",
  "tags": ["programming", "python"],
  "priority": "high",
  "start_date": "2024-01-01",
  "target_date": "2024-04-01"
}
```

### Add Milestone

**POST** `/api/goals/goals/{id}/add_milestone/`

Request:
```json
{
  "title": "Complete beginner course",
  "description": "Finish the Python basics course",
  "target_date": "2024-02-01",
  "order": 1
}
```

### Add Progress Update

**POST** `/api/goals/goals/{id}/add_progress/`

Request:
```json
{
  "update_text": "Completed 3 chapters today",
  "progress_percentage": 35,
  "mood": "motivated"
}
```

### Report Setback

**POST** `/api/goals/goals/{id}/report_setback/`

Request:
```json
{
  "description": "Had to pause learning due to work commitments",
  "severity": "moderate",
  "setback_type": "time_constraint"
}
```

## Coaching

### Create Coaching Session

**POST** `/api/coaching/sessions/`

Request:
```json
{
  "session_type": "check_in",
  "title": "Weekly Check-in",
  "goal": 1,
  "context": {
    "automated": false
  }
}
```

### Add Message to Session

**POST** `/api/coaching/sessions/{id}/add_message/`

Request:
```json
{
  "role": "user",
  "content": "I'm feeling stuck with my goal"
}
```

### Complete Session

**POST** `/api/coaching/sessions/{id}/complete/`

Request:
```json
{
  "outcome_summary": "Discussed strategies for overcoming obstacles",
  "action_items": [
    "Break down goal into smaller steps",
    "Schedule 30 minutes daily for practice"
  ],
  "insights_gained": [
    "User responds better to morning sessions"
  ]
}
```

## AI Agents

### Generate AI Response

**POST** `/api/agents/ai/generate_response/`

Request:
```json
{
  "message": "How can I stay motivated?",
  "context": {
    "goals": [...],
    "progress": {...},
    "mood": "neutral"
  }
}
```

Response:
```json
{
  "response": "I understand you're looking for motivation...",
  "reasoning": "Based on your progress and coaching style preference...",
  "confidence": 0.85,
  "model": "gemini-pro"
}
```

### Analyze Setback

**POST** `/api/agents/ai/analyze_setback/`

Request:
```json
{
  "description": "Missed 3 days of practice",
  "goal_id": 1
}
```

Response:
```json
{
  "analysis": "Root cause appears to be time management...",
  "recovery_plan": [
    "Reschedule practice sessions",
    "Set reminders",
    "Start with 15 minutes instead of 30"
  ],
  "timeline_adjustment": "Extend deadline by 1 week",
  "reasoning": "...",
  "confidence": 0.82
}
```

### Get Agent Statistics

**GET** `/api/agents/decisions/statistics/`

Response:
```json
{
  "total_decisions": 156,
  "decisions_by_type": {
    "strategy_selection": 45,
    "intervention_trigger": 32,
    "encouragement": 79
  },
  "average_confidence": 0.83,
  "most_common_model": {
    "model_name": "gemini-pro",
    "count": 156
  }
}
```

## WebSocket

### Connect to Coaching Session

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/coaching/1/');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Message:', data);
};

// Send message
ws.send(JSON.stringify({
  type: 'message',
  message: 'Hello coach!'
}));
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message here"
}
```

Common status codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error
