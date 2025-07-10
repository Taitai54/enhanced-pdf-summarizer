# Quick Start Guide - Enhanced PDF Summarizer

## 🚀 One-Time Setup (Do This Once)

### Step 1: Install Ollama on Windows
1. Download from: https://ollama.com/download
2. Install the Windows version
3. Download AI models (run in Windows Command Prompt):
   ```cmd
   ollama pull llama3.2:3b
   ollama pull mistral:7b
   ollama pull llama3.2:1b
   ```

### Step 2: Setup Complete!
Your setup is now ready to use anytime.

---

## 🎯 Every Time You Want to Use It

### Step 1: Start Ollama (Windows)
Open **Windows Command Prompt** and run:
```cmd
set OLLAMA_HOST=0.0.0.0:11434
ollama serve
```
*Keep this window open while using the app*

### Step 2: Start PDF Summarizer (WSL)
Open **WSL Terminal** and run:
```bash
cd /mnt/c/Users/matti/GitHub
source pdf_summarizer_env/bin/activate
python enhanced_pdf_app.py
```

### Step 3: Open Your Browser
Go to: **http://localhost:8511**

### Step 4: Use the App
- Upload single or multiple PDFs
- Choose summary length and style
- Download results as PDF or ZIP files

---

## 🔧 Troubleshooting

### Ollama Not Connected?
- Make sure Ollama is running with `set OLLAMA_HOST=0.0.0.0:11434`
- Check Windows Command Prompt shows: `Listening on [::]:11434`

### App Won't Load?
- Try a different port: `python enhanced_pdf_app.py` (it will show the port)
- Use `http://127.0.0.1:8511` instead of `localhost`

### Want to Stop?
- **Ollama**: Press `Ctrl+C` in Windows Command Prompt
- **PDF App**: Press `Ctrl+C` in WSL Terminal

---

## 📱 Features Available

✅ **Multiple PDF Upload** - Process many files at once  
✅ **Custom Summary Lengths** - From 200 to 2000+ words  
✅ **Different Styles** - Bullet points, executive summary, technical analysis  
✅ **Download Options** - Individual PDFs, ZIP files, combined summaries  
✅ **Progress Tracking** - See processing status  
✅ **Model Selection** - Choose different AI models  

---

## 💡 Pro Tips

- **Faster Processing**: Use `llama3.2:1b` for quicker summaries
- **Better Quality**: Use `llama3.2:3b` or `mistral:7b` for detailed analysis
- **Batch Processing**: Upload multiple PDFs and get a ZIP file with all summaries
- **Custom Instructions**: Add specific prompts like "Focus on financial data" or "Extract key findings"

---

## 🆘 Need Help?

If something doesn't work:
1. Check that Ollama shows `Listening on [::]:11434`
2. Make sure virtual environment is activated
3. Try restarting both services
4. Check browser console for errors

**Happy Summarizing!** 🎉