# PDF Summarizer with Ollama - Setup Instructions

This updated version uses Ollama for local LLM processing, eliminating the need for external API keys.

## Quick Start (Recommended)

### Option 1: Using Docker Compose (Easiest)

1. **Install Docker and Docker Compose**
   - Download Docker Desktop from https://www.docker.com/products/docker-desktop/
   - Ensure Docker Compose is included (it comes with Docker Desktop)

2. **Run the setup script**
   ```bash
   cd /mnt/c/Users/matti/GitHub
   ./setup_ollama.sh
   ```

3. **Access the application**
   - PDF Summarizer: http://localhost:8501
   - Ollama API: http://localhost:11434

### Option 2: Manual Docker Setup

1. **Start services**
   ```bash
   cd /mnt/c/Users/matti/GitHub
   docker-compose up -d
   ```

2. **Pull models** (wait for Ollama to start first)
   ```bash
   docker exec ollama ollama pull llama3.2:3b
   docker exec ollama ollama pull llama3.2:1b  # Faster alternative
   ```

3. **Check models**
   ```bash
   docker exec ollama ollama list
   ```

## Manual Installation (Without Docker)

### 1. Install Ollama

**For Windows:**
- Download from https://ollama.com/download
- Run the installer

**For Linux/WSL:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Start Ollama
```bash
ollama serve
```

### 3. Pull Models
```bash
ollama pull llama3.2:3b      # Good balance of speed/quality
ollama pull llama3.2:1b      # Faster, smaller model
ollama pull mistral:7b       # Alternative model
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
streamlit run pdf_summarizer.py
```

## Features

✅ **No API Keys Required** - Everything runs locally
✅ **File Upload Interface** - Click to select PDF files
✅ **Custom Instructions** - Add your own summarization prompts
✅ **Model Selection** - Choose from available Ollama models
✅ **Real-time Processing** - See the progress and debug info
✅ **PDF Output** - Download summaries as formatted PDFs

## Usage

1. **Select PDF Files**: Click the upload button to select your PDF files
2. **Choose Model**: Select from available Ollama models
3. **Set Parameters**: Adjust summary length (200-2000 words)
4. **Custom Instructions**: (Optional) Add custom prompts like:
   - "Summarize in bullet points: {text}"
   - "Extract key findings from: {text}"
   - "Create an executive summary of: {text}"
5. **Generate**: Click "Generate Summaries" to process
6. **Download**: Download the generated summary PDFs

## Recommended Models

- **llama3.2:3b** - Good balance of speed and quality (default)
- **llama3.2:1b** - Faster processing, smaller model
- **mistral:7b** - Alternative model, good for longer texts

## Troubleshooting

### Docker Issues
```bash
# Stop services
docker-compose down

# Remove containers and start fresh
docker-compose down -v
docker-compose up -d

# View logs
docker-compose logs -f
```

### Manual Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve

# Check available models
ollama list
```

### Performance Tips
- Use smaller models (llama3.2:1b) for faster processing
- Reduce summary length for quicker results
- Process fewer files at once for better performance

## File Structure

```
├── pdf_summarizer.py       # Main application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker services
├── setup_ollama.sh        # Automated setup script
├── .dockerignore          # Docker ignore patterns
└── README_OLLAMA_SETUP.md # This file
```

## Stopping the Application

### Docker:
```bash
docker-compose down
```

### Manual:
- Stop Streamlit: `Ctrl+C`
- Stop Ollama: `pkill ollama`

## System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB+ for models
- **CPU**: Modern multi-core processor
- **GPU**: Optional, can speed up processing