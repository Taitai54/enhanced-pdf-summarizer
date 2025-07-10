#!/bin/bash

# Enhanced PDF Summarizer - Quick Start Script
# This script starts the PDF summarizer application

echo "🚀 Starting Enhanced PDF Summarizer..."
echo "=================================="

# Get the script directory and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "enhanced_pdf_app.py" ]; then
    echo "❌ Error: enhanced_pdf_app.py not found"
    echo "   Make sure you're in the enhanced-pdf-summarizer directory"
    exit 1
fi

# Check if virtual environment exists (look in parent directory too)
if [ -d "pdf_summarizer_env" ]; then
    echo "📦 Activating virtual environment..."
    source pdf_summarizer_env/bin/activate
elif [ -d "../pdf_summarizer_env" ]; then
    echo "📦 Activating virtual environment from parent directory..."
    source ../pdf_summarizer_env/bin/activate
else
    echo "⚠️  No virtual environment found, using system Python"
    echo "   For better isolation, create a virtual environment:"
    echo "   python3 -m venv pdf_summarizer_env"
    echo "   source pdf_summarizer_env/bin/activate"
    echo "   pip install -r requirements.txt"
fi

# Check if Ollama is accessible
echo "🔍 Checking Ollama connection..."
if curl -s --connect-timeout 3 http://172.24.64.1:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running and accessible!"
elif curl -s --connect-timeout 3 http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running on localhost!"
else
    echo "⚠️  Warning: Ollama is not accessible"
    echo "   Make sure to run in Windows Command Prompt:"
    echo "   set OLLAMA_HOST=0.0.0.0:11434"
    echo "   ollama serve"
    echo ""
    echo "   Starting PDF app anyway..."
fi

# Find available port
PORT=8511
while netstat -ln 2>/dev/null | grep -q ":$PORT "; do
    PORT=$((PORT + 1))
done

echo "🌐 Starting PDF Summarizer on port $PORT..."
echo "📱 Open your browser to: http://localhost:$PORT"
echo ""
echo "Features available:"
echo "  ✅ Multiple PDF upload and batch processing"
echo "  ✅ Custom summary lengths and styles"
echo "  ✅ AI model selection (if multiple models available)"
echo "  ✅ Download summaries as PDF or ZIP files"
echo "  ✅ Progress tracking and error handling"
echo ""
echo "⏹️  Press Ctrl+C to stop the application"
echo "=================================="

# Start the application
python enhanced_pdf_app.py

echo ""
echo "👋 PDF Summarizer stopped. Thank you!"