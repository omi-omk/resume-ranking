#!/bin/bash

echo "Starting Resume Ranking Application..."

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "Starting MongoDB..."
    sudo systemctl start mongodb || brew services start mongodb-community || echo "Please start MongoDB manually"
    sleep 3
fi

# Check if .env files exist
if [ ! -f "analysis_service/.env" ]; then
    echo "Creating analysis_service/.env from example..."
    cp analysis_service/.env.example analysis_service/.env
    echo "Please edit analysis_service/.env and add your GEMINI_API_KEY"
fi

if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env from example..."
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "Creating frontend/.env.local..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:5000" > frontend/.env.local
fi

# Install dependencies if node_modules don't exist
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm run install:all
fi

echo "Starting all services..."
npm run dev