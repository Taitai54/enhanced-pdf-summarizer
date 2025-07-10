@echo off
REM Enhanced PDF Summarizer - Ollama Starter Script for Windows
REM This script starts Ollama with the correct network settings

echo 🚀 Starting Ollama for PDF Summarizer...
echo =====================================

echo 📡 Setting up network access...
set OLLAMA_HOST=0.0.0.0:11434

echo 🤖 Starting Ollama server...
echo.
echo ✅ Ollama is now running and accessible from WSL
echo 🌐 You can now start the PDF Summarizer in WSL
echo.
echo ⏹️  Press Ctrl+C to stop Ollama
echo =====================================

ollama serve

echo.
echo 👋 Ollama stopped. Thank you!