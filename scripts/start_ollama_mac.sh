#!/bin/bash

# Enhanced PDF Summarizer - Ollama Starter Script for macOS
# This script starts Ollama with the correct settings for macOS

echo "🚀 Starting Ollama for PDF Summarizer (macOS)..."
echo "============================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo ""
    echo "Install options:"
    echo "1. Homebrew: brew install ollama"
    echo "2. Direct: curl -fsSL https://ollama.com/install.sh | sh"
    echo "3. Download: https://ollama.com/download"
    exit 1
fi

# Check if any models are available
echo "🔍 Checking available models..."
if ! ollama list | grep -q "NAME"; then
    echo "⚠️  No models found. Downloading recommended model..."
    echo "📥 Pulling llama3.2:3b (this may take a few minutes)..."
    ollama pull llama3.2:3b
fi

echo "📡 Starting Ollama server..."
echo ""
echo "✅ Ollama is now running and accessible"
echo "🌐 PDF Summarizer can now connect to Ollama"
echo "📱 You can start the PDF app in another terminal:"
echo "   ./scripts/start_pdf_summarizer.sh"
echo ""
echo "⏹️  Press Ctrl+C to stop Ollama"
echo "============================================="

# Start Ollama - on macOS it usually binds to all interfaces by default
ollama serve

echo ""
echo "👋 Ollama stopped. Thank you!"