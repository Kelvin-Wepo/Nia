# Nia - AI Goal Coaching Platform

An agentic AI goal coaching platform that helps users achieve goals by adapting to real human behavior, recovering from setbacks, and providing transparent reasoning for all decisions.

## Features

- **Adaptive AI Coaching**: Personalized coaching that learns from user behavior and adjusts strategies
- **Transparent Decision-Making**: See the reasoning behind every AI decision
- **Setback Recovery**: AI-powered recovery plans when things don't go as planned
- **Real-time Coaching**: WebSocket-based live coaching sessions
- **Progress Tracking**: Comprehensive goal and milestone tracking
- **Agent Observability**: Full transparency with Opik SDK integration
- **Behavioral Learning**: AI learns from user patterns to provide better guidance

## Tech Stack

### Backend
- **Django 5.0+** with Django REST Framework
- **PostgreSQL** for data persistence
- **Redis** for caching and message broker
- **Celery** for background tasks
- **Django Channels** for WebSocket support
- **Gemini AI** for intelligent coaching
- **Opik SDK** for agent observability

### Frontend
- **React 18+** with TypeScript
- **Vite** for fast development
- **TailwindCSS** for styling
- **React Query** for data fetching
- **Zustand** for state management
- **React Router** for navigation

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Nia
```

### 2. Backend Setup

#### Create and activate virtual environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r ../requirements.txt
```

#### Set up environment variables
```bash
cp ../.env.example .env
```

Edit `.env` and configure:
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `GEMINI_API_KEY`: Your Gemini API key
- `OPIK_API_KEY`: Your Opik API key

#### Create PostgreSQL database
```bash
createdb nia_db
# Or use psql:
# psql -U postgres
# CREATE DATABASE nia_db;
# CREATE USER nia_user WITH PASSWORD 'nia_password';
# GRANT ALL PRIVILEGES ON DATABASE nia_db TO nia_user;
```

#### Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create superuser
```bash
python manage.py createsuperuser
```

#### Start the development server
```bash
python manage.py runserver
```

#### Start Celery worker (in a new terminal)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
celery -A config worker -l info
```

#### Start Celery beat (in another terminal)
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
celery -A config beat -l info
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/users/register/` - Register new user
- `GET /api/users/me/` - Get current user profile

### Goals
- `GET /api/goals/goals/` - List all goals
- `POST /api/goals/goals/` - Create a new goal
- `GET /api/goals/goals/{id}/` - Get goal details
- `PATCH /api/goals/goals/{id}/` - Update goal
- `DELETE /api/goals/goals/{id}/` - Delete goal
- `POST /api/goals/goals/{id}/add_milestone/` - Add milestone
- `POST /api/goals/goals/{id}/add_progress/` - Add progress update
- `POST /api/goals/goals/{id}/report_setback/` - Report setback

### Coaching
- `GET /api/coaching/sessions/` - List coaching sessions
- `POST /api/coaching/sessions/` - Create session
- `GET /api/coaching/sessions/{id}/` - Get session details
- `POST /api/coaching/sessions/{id}/complete/` - Complete session
- `GET /api/coaching/interventions/` - List interventions
- `POST /api/coaching/interventions/{id}/feedback/` - Provide feedback

### AI Agents
- `GET /api/agents/decisions/` - List agent decisions
- `GET /api/agents/decisions/recent/` - Get recent decisions
- `GET /api/agents/decisions/statistics/` - Get decision statistics
- `GET /api/agents/learning/` - List learning records
- `GET /api/agents/metrics/summary/` - Get performance metrics
- `POST /api/agents/ai/generate_response/` - Generate AI response
- `POST /api/agents/ai/analyze_setback/` - Analyze setback
- `POST /api/agents/ai/suggest_strategy/` - Suggest strategy

### WebSocket
- `ws://localhost:8000/ws/coaching/{session_id}/` - Coaching session WebSocket

## Project Structure

```
Nia/
├── backend/
│   ├── config/              # Django settings and configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── celery.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── users/               # User management
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   ├── goals/               # Goal tracking
│   │   ├── models.py        # Goal, Milestone, ProgressUpdate, Setback
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tasks.py         # Celery tasks
│   │   └── urls.py
│   ├── coaching/            # Coaching sessions
│   │   ├── models.py        # CoachingSession, Message, Intervention
│   │   ├── views.py
│   │   ├── consumers.py     # WebSocket consumers
│   │   ├── routing.py
│   │   ├── tasks.py
│   │   └── urls.py
│   ├── agents/              # AI agents and decisions
│   │   ├── models.py        # AgentDecision, LearningRecord
│   │   ├── views.py
│   │   ├── gemini_service.py    # Gemini AI integration
│   │   ├── opik_service.py      # Opik observability
│   │   └── urls.py
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/           # Page components
│   │   ├── lib/             # API client, utilities
│   │   ├── store/           # Zustand stores
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── requirements.txt
├── .env.example
└── README.md
```

## AI Features

### Gemini Integration
The platform uses Google's Gemini AI for:
- **Coaching Responses**: Context-aware, personalized coaching messages
- **Setback Analysis**: Root cause analysis and recovery planning
- **Strategy Adjustment**: Adaptive strategy recommendations
- **Intervention Generation**: Proactive coaching interventions

### Opik Observability
All AI decisions are tracked with Opik for:
- **Decision Transparency**: See reasoning chains for every decision
- **Performance Metrics**: Track effectiveness and user satisfaction
- **A/B Testing**: Experiment with different strategies
- **Learning Validation**: Validate what the AI learns over time

## Database Models

### Core Models
- **User**: Extended Django user with coaching preferences
- **Goal**: User goals with progress tracking
- **Milestone**: Sub-goals within larger goals
- **ProgressUpdate**: Regular progress check-ins
- **Setback**: Challenges and recovery tracking
- **CoachingSession**: AI coaching conversations
- **Message**: Individual messages in sessions
- **Intervention**: Proactive AI interventions
- **AgentDecision**: Transparent AI decision records
- **LearningRecord**: What AI learns about users

## Background Tasks

### Celery Tasks
- **check_goal_progress**: Monitor goal progress and trigger interventions
- **update_goal_predictions**: Update AI predictions for goals
- **analyze_user_behavior_patterns**: Learn from user behavior
- **send_daily_check_ins**: Send scheduled check-ins
- **generate_session_summary**: Summarize completed sessions

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Environment Variables

### Required
- `SECRET_KEY`: Django secret key
- `GEMINI_API_KEY`: Google Gemini API key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string

### Optional
- `DEBUG`: Enable debug mode (default: False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `OPIK_API_KEY`: Opik API key for observability
- `OPIK_WORKSPACE`: Opik workspace name

## Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure proper `ALLOWED_HOSTS`
3. Use a production WSGI server (Gunicorn)
4. Set up PostgreSQL and Redis
5. Configure Celery with systemd or supervisor
6. Serve static files with Nginx or CDN

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Serve the `dist` folder with Nginx or CDN
3. Configure API base URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review API endpoints

## Roadmap

- [ ] Mobile app (React Native)
- [ ] Voice coaching interface
- [ ] Integration with wearables
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Community features
- [ ] Goal templates marketplace

## Acknowledgments

- Django and DRF teams
- React and Vite teams
- Google Gemini team
- Opik SDK team
- All open-source contributors
