#!/bin/bash

echo "Setting up Ollama for Resume Ranking Application..."

# Start Ollama container
echo "Starting Ollama container..."
docker compose up -d ollama

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull the Llama 3.1 model
echo "Pulling Llama 3.1 model (this may take a while)..."
docker exec ollama ollama pull llama3.1

echo "Ollama setup complete!"
echo "You can now start the full application with: docker compose up -d"