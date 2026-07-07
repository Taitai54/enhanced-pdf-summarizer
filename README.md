# Enhanced PDF Summarizer

A powerful web-based PDF summarization tool that uses local AI models (via Ollama) to generate intelligent summaries of PDF documents. Supports batch processing, multiple output formats, and customizable summary styles.

## Features

- **Batch Processing**: Process multiple PDF files simultaneously
- **AI-Powered Summaries**: Uses Ollama with customizable AI models (default: llama3.2:3b)
- **Flexible Summary Options**:
  - Multiple length presets (short, medium, long, very long, custom)
  - Various styles (comprehensive, bullet points, executive, technical, key findings)
  - Custom instructions for targeted summaries
- **Multiple Output Formats**:
  - Text-only display
  - PDF document generation
  - Combined batch summaries
  - ZIP archives for batch downloads
- **User-Friendly Interface**: Clean web UI with progress tracking and real-time status updates

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running locally
- At least one Ollama model pulled (recommended: `llama3.2:3b`)

## Installation

1. Clone or download this repository

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is installed and running:
```bash
# Pull a model if you haven't already
ollama pull llama3.2:3b

# Start Ollama (if not already running)
ollama serve
```

## Usage

1. Start the server:
```bash
python enhanced_pdf_app.py
```

2. Open your browser to: `http://localhost:8511`

3. The interface will automatically check Ollama status and display available models

4. Select one or more PDF files and configure your summary preferences:
   - Choose summary length
   - Select AI model
   - Pick output format
   - Choose summary style
   - Add custom instructions (optional)

5. Click "Process PDF(s)" and wait for the summaries to generate

6. Download individual summaries or batch download all results

## Configuration

### Port
The default port is `8511`. To change it, modify the `PORT` variable in `enhanced_pdf_app.py`:
```python
PORT = 8511  # Change to your preferred port
```

### Ollama URLs
The application checks multiple Ollama endpoints automatically:
- `http://localhost:11434`
- `http://127.0.0.1:11434`
- `http://172.24.64.1:11434` (WSL2 support)

### AI Models
Any Ollama model can be used. The dropdown will populate with all available models on your system.

## Summary Options

### Length Presets
- **Short**: 200-300 words
- **Medium**: 500-700 words (default)
- **Long**: 1000-1500 words
- **Very Long**: 2000+ words
- **Custom**: Specify exact word count

### Summary Styles
- **Comprehensive**: Full overview covering all major points
- **Bullet Points**: Structured key information
- **Executive**: Focus on decisions and outcomes
- **Technical**: Detailed methodologies and specifications
- **Key Findings**: Most important conclusions only
- **Custom**: Use custom instructions field

### Batch Modes
- **Individual**: Separate summary for each PDF
- **Combined**: Single summary combining all documents
- **Comparison**: Comparative analysis across documents

## Output Formats

- **Text Only**: Display summaries in the browser
- **PDF Document**: Generate downloadable PDF summaries
- **Both**: Text display + PDF download option
- **ZIP Archive**: Download all summaries in a single ZIP file (batch processing)

## Troubleshooting

### Ollama Not Found
- Ensure Ollama is installed and running: `ollama serve`
- Check that at least one model is available: `ollama list`
- Verify Ollama is accessible at `http://localhost:11434`

### PDF Processing Errors
- Ensure PDF files contain extractable text (not scanned images)
- Check file size - very large PDFs may take longer to process
- Verify sufficient disk space for temporary files

### Timeout Issues
- Large PDFs or complex summaries may take time
- Default timeout is 300 seconds (5 minutes)
- Consider using shorter summary lengths for faster processing

## Dependencies

- `streamlit>=1.28.0` - Web framework
- `PyPDF2>=3.0.0` - PDF text extraction
- `requests>=2.31.0` - HTTP client for Ollama API
- `reportlab>=4.0.0` - PDF generation
- `pathlib` - File path handling
- `python-dotenv` - Environment configuration

## License

See LICENSE file for details.

## Notes

- Temporary files are stored in the system temp directory
- PDF summaries include timestamps for organization
- The application runs a local HTTP server - no data is sent to external services
- All AI processing happens locally via Ollama
