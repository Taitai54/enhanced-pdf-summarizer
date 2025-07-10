#!/bin/bash

# Script to set up Ollama and pull required models

echo "Setting up Ollama and PDF Summarizer..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start Ollama service
echo "Starting Ollama service..."
docker-compose up -d ollama

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
sleep 10

# Check if Ollama is running
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
    fi
    echo "Attempt $attempt/$max_attempts: Waiting for Ollama..."
    sleep 5
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Ollama failed to start after $max_attempts attempts."
    exit 1
fi

# Pull the default model
echo "Pulling Llama 3.2 3B model (this may take a while)..."
docker exec ollama ollama pull llama3.2:3b

# Pull additional useful models
echo "Pulling additional models..."
docker exec ollama ollama pull llama3.2:1b  # Faster, smaller model
docker exec ollama ollama pull mistral:7b   # Alternative model

# List available models
echo "Available models:"
docker exec ollama ollama list

# Start the PDF summarizer service
echo "Starting PDF Summarizer service..."
docker-compose up -d pdf-summarizer

echo "Setup complete!"
echo "PDF Summarizer is available at: http://localhost:8501"
echo "Ollama API is available at: http://localhost:11434"
echo ""
echo "To stop the services: docker-compose down"
echo "To view logs: docker-compose logs -f"