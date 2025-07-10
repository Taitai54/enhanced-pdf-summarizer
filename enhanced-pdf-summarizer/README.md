# Enhanced PDF Summarizer with Ollama

A powerful, local AI-powered PDF summarizer that processes multiple documents with customizable output formats and batch processing capabilities.

## 🚀 Features

- **🔄 Batch Processing** - Upload and process multiple PDFs simultaneously
- **🤖 AI Model Selection** - Choose from various Ollama models (llama3.2, mistral, etc.)
- **📏 Custom Summary Lengths** - From 200 words to 2000+ words
- **🎨 Multiple Styles** - Bullet points, executive summary, technical analysis, key findings
- **📱 User-Friendly Interface** - Clean web interface with progress tracking
- **💾 Download Options** - Individual PDFs, ZIP archives, or combined summaries
- **🔒 Privacy-First** - Everything runs locally, no data sent to external services
- **⚡ Fast Processing** - Optimized for performance with progress indicators

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Ollama** installed on your system
- **Operating System:** Windows/WSL2, macOS, or Linux

## 🖥️ Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **macOS** | ✅ Fully Supported | Native Ollama support, easy setup |
| **Linux** | ✅ Fully Supported | All features available |
| **Windows/WSL2** | ✅ Tested | Requires network configuration |
| **Windows Native** | ⚠️ Partial | Python app works, may need path adjustments |

## 🛠️ Quick Setup

### 1. Install Ollama

**macOS:**
```bash
# Option 1: Homebrew (recommended)
brew install ollama

# Option 2: Direct download
curl -fsSL https://ollama.com/install.sh | sh

# Option 3: Download from https://ollama.com/download
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
- Download installer from https://ollama.com/download

### 2. Download AI Models
```bash
ollama pull llama3.2:3b      # Recommended default
ollama pull llama3.2:1b      # Faster, smaller model
ollama pull mistral:7b       # Higher quality, slower
```

### 3. Clone and Setup
```bash
git clone <your-repo-url>
cd enhanced-pdf-summarizer
pip install -r requirements.txt
```

### 4. Run the Application

**macOS/Linux:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start PDF Summarizer
./scripts/start_pdf_summarizer.sh
# OR manually:
python enhanced_pdf_app.py
```

**Windows:**
```cmd
# Terminal 1: Start Ollama
scripts\start_ollama.cmd

# Terminal 2: Start PDF Summarizer (WSL)
./scripts/start_pdf_summarizer.sh
```

**Manual startup (all platforms):**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start PDF Summarizer
python enhanced_pdf_app.py
```

### 5. Access the Application
Open your browser to: **http://localhost:8511**

## 📖 Usage

1. **Upload PDFs** - Select single or multiple PDF files
2. **Choose AI Model** - Select from available Ollama models
3. **Customize Summary** - Set length, style, and custom instructions
4. **Process** - Watch real-time progress as files are processed
5. **Download** - Get individual PDFs, ZIP files, or combined summaries

## 🎯 Summary Options

### Length Options
- **Short** (200-300 words)
- **Medium** (500-700 words)
- **Long** (1000-1500 words)
- **Very Long** (2000+ words)
- **Custom** (specify exact word count)

### Style Options
- **Comprehensive** - Complete overview of all content
- **Bullet Points** - Structured key points
- **Executive Summary** - Decision-focused summary
- **Technical Analysis** - Detailed technical breakdown
- **Key Findings** - Important conclusions only

### Output Formats
- **Text** - Plain text summaries
- **PDF** - Formatted PDF documents
- **ZIP** - Batch download all summaries
- **Combined** - Single document with all summaries

## 🔧 Configuration

### Ollama Models
The application automatically detects available models. Popular options:

- `llama3.2:1b` - Fastest processing
- `llama3.2:3b` - Balanced speed/quality (recommended)
- `mistral:7b` - Best quality analysis
- `codellama:7b` - Technical document analysis

### Custom Prompts
Add specific instructions like:
- "Focus on financial data and metrics"
- "Extract methodology and conclusions"
- "Summarize in bullet points with action items"
- "Compare findings across documents"

## 📁 Project Structure

```
enhanced-pdf-summarizer/
├── enhanced_pdf_app.py          # Main application
├── requirements.txt             # Python dependencies
├── scripts/
│   ├── start_ollama.cmd        # Windows Ollama starter
│   └── start_pdf_summarizer.sh # Linux/WSL app starter
├── docs/
│   ├── QUICK_START.md          # Detailed setup guide
│   ├── MACOS_SETUP.md          # macOS-specific instructions
│   ├── README_SIMPLE.md        # Copy-paste instructions
│   └── README_OLLAMA_SETUP.md  # Ollama configuration
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── working_pdf_app.py          # Alternative simple version
├── simple_server.py            # Basic HTTP server version
└── test_simple.py              # Testing utilities
```

## 🐛 Troubleshooting

### Common Issues

**"Ollama not connected"**
- Ensure Ollama is running: `ollama serve`
- Check network binding: `export OLLAMA_HOST=0.0.0.0:11434`
- Verify models are downloaded: `ollama list`

**"Port already in use"**
- The app automatically finds available ports
- Manually specify: `python enhanced_pdf_app.py --port 8512`

**"No models available"**
- Download models: `ollama pull llama3.2:3b`
- Check Ollama is accessible: `curl http://localhost:11434/api/tags`

### Performance Tips
- Use `llama3.2:1b` for faster processing
- Process fewer files simultaneously for better performance
- Reduce summary length for quicker results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.com/) for local AI processing
- Uses [PyPDF2](https://pypdf2.readthedocs.io/) for PDF text extraction
- [ReportLab](https://www.reportlab.com/) for PDF generation
- Interface powered by vanilla JavaScript and HTML5

## 📞 Support

For issues and questions:
1. **macOS users:** Check the [macOS setup guide](docs/MACOS_SETUP.md)
2. **General:** Review [setup instructions](docs/QUICK_START.md)  
3. **Quick start:** Check the [troubleshooting guide](docs/README_SIMPLE.md)
4. Create an issue in this repository

---

**🎉 Happy Summarizing!** Process your PDFs with the power of local AI.