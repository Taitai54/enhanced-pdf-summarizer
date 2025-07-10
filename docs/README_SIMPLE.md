# Enhanced PDF Summarizer - Simple Instructions

## 🎯 How to Use (Copy & Paste These Commands)

### Every Time You Want to Use the PDF Summarizer:

**1. Start Ollama (Windows Command Prompt):**
```cmd
cd /d C:\Users\matti\GitHub
start_ollama.cmd
```

**2. Start PDF App (WSL Terminal):**
```bash
cd /mnt/c/Users/matti/GitHub
./start_pdf_summarizer.sh
```

**3. Open Browser:**
Go to: **http://localhost:8511**

---

## 🔧 Available AI Models

You can now select different AI models in the app:

- **llama3.2:1b** - Fastest, good for quick summaries
- **llama3.2:3b** - Balanced speed and quality (recommended)
- **mistral:7b** - Best quality, slower processing

To download more models, run in Windows Command Prompt:
```cmd
ollama pull llama3.2:1b
ollama pull mistral:7b
ollama pull codellama:7b
```

---

## 📁 Files Created

✅ **enhanced_pdf_app.py** - Main application with all features  
✅ **QUICK_START.md** - Detailed setup instructions  
✅ **start_pdf_summarizer.sh** - One-click WSL startup script  
✅ **start_ollama.cmd** - One-click Windows Ollama starter  
✅ **Git repository** - All files committed to local Git  

---

## 🚀 Features

- **Multiple PDF Upload** - Process many files at once
- **AI Model Selection** - Choose the best model for your needs
- **Custom Summary Lengths** - 200 words to 2000+ words
- **Different Styles** - Bullet points, executive summary, technical analysis
- **Download Options** - PDF, ZIP, combined summaries
- **Batch Processing** - Progress tracking and error handling

---

## 🆘 Quick Troubleshooting

- **"Ollama not connected"** → Run `start_ollama.cmd` in Windows
- **"Port already in use"** → The script will find a free port automatically
- **"Models not showing"** → Make sure Ollama is running with models downloaded

**That's it! You're ready to summarize PDFs with AI!** 🎉