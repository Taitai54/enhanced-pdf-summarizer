# 📚 PDF Summarizer – Local Setup Guide (macOS)

This guide walks you through setting up the Enhanced PDF Summarizer project locally on a Mac, using either Python 3.11 (recommended) or Python 3.13+ with minor code edits.

---

## ✅ Recommended Setup: Python 3.11.9 with Virtual Environment

### 1. Install pyenv and Python 3.11
```bash
brew install pyenv
pyenv install 3.11.9
cd /Users/matt.atkinson/Documents/GitHub/enhanced-pdf-summarizer
pyenv local 3.11.9
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv pdf_summarizer_env
source pdf_summarizer_env/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚠️ If You're Using Python 3.13 or Later

Python 3.13+ removed the `cgi` module, so you need to remove deprecated imports.

### Steps to Patch the Code
1. Open the main app file:
```bash
nano enhanced_pdf_app.py
```

2. Comment out or remove this line:
```python
import cgi
```

3. Also remove or replace any lines like:
```python
cgi.escape(...)
cgi.FieldStorage()
```

Then save and exit (`Ctrl + O`, `Enter`, `Ctrl + X` in nano).

---

## 🚀 Run the Application

### 1. Start Ollama (if not already running)
```bash
ollama serve
```

> If you see `Error: bind: address already in use`, Ollama is already running. You can skip this.

---

### 2. Launch the PDF Summarizer
```bash
./scripts/start_pdf_summarizer.sh
```

---

## 🌐 Access the App

Open your browser to:

```
http://localhost:8511
```

You can now:
- Upload one or more PDFs
- Choose summary length/style
- Select a model (e.g. `llama3`)
- Download the result as PDF/ZIP
- Track live progress

---

## ✅ Quick Reference Summary

```bash
cd /Users/matt.atkinson/Documents/GitHub/enhanced-pdf-summarizer
python3 -m venv pdf_summarizer_env
source pdf_summarizer_env/bin/activate
pip install -r requirements.txt
ollama serve
./scripts/start_pdf_summarizer.sh
```

---

## 🧠 Need Automation?

To expose this for automation (e.g. via n8n, webhook, or browser-based UI), reverse proxy setup, or external hosting, raise an issue or request support.
