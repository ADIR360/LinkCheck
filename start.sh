#!/bin/bash

# Click Tracker Startup Script

echo "🚀 Starting Click Tracker..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Set default environment variables
export BASE_URL=${BASE_URL:-"http://localhost:8000"}
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-"8000"}
export DEBUG=${DEBUG:-"true"}

echo "🌐 Starting server on $HOST:$PORT"
echo "📊 Dashboard: $BASE_URL"
echo "🔗 API: $BASE_URL/api/links"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the application
python backend/app.py
