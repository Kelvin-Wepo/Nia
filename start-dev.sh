#!/bin/bash

echo "🚀 Starting Nia Development Environment..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
echo "📦 Installing backend dependencies..."
cd backend
source venv/bin/activate
pip install -q -r ../requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp ../.env.example .env
    echo "⚠️  Please update .env with your API keys and database credentials"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Start Django server in background
echo "🌐 Starting Django server..."
python manage.py runserver > /dev/null 2>&1 &
DJANGO_PID=$!

# Start Celery worker in background
echo "⚙️  Starting Celery worker..."
celery -A config worker -l info > /dev/null 2>&1 &
CELERY_PID=$!

cd ..

# Install frontend dependencies and start
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --silent

echo "🎨 Starting React development server..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "✅ Nia is now running!"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:3000"
echo "📍 Admin:    http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $DJANGO_PID $CELERY_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
