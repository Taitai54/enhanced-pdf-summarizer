# macOS Setup Guide - Enhanced PDF Summarizer

## 🍎 Quick Setup for macOS

### Step 1: Install Prerequisites

**Install Homebrew (if not already installed):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Install Python (if needed):**
```bash
brew install python
```

**Install Ollama:**
```bash
# Option 1: Homebrew (recommended)
brew install ollama

# Option 2: Direct download
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Download the Project
```bash
git clone https://github.com/yourusername/enhanced-pdf-summarizer.git
cd enhanced-pdf-summarizer
```

### Step 3: Setup Python Environment
```bash
# Create virtual environment
python3 -m venv pdf_summarizer_env

# Activate virtual environment
source pdf_summarizer_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Download AI Models
```bash
ollama pull llama3.2:3b      # Recommended default (2GB)
ollama pull llama3.2:1b      # Faster, smaller model (1.3GB)
ollama pull mistral:7b       # Higher quality (4.1GB)
```

---

## 🚀 Running the Application

### Method 1: Using Scripts (Recommended)

**Terminal 1 (Start Ollama):**
```bash
./scripts/start_ollama_mac.sh
```

**Terminal 2 (Start PDF App):**
```bash
./scripts/start_pdf_summarizer.sh
```

### Method 2: Manual Start

**Terminal 1:**
```bash
ollama serve
```

**Terminal 2:**
```bash
source pdf_summarizer_env/bin/activate
python enhanced_pdf_app.py
```

### Step 5: Access the App
Open Safari, Chrome, or your preferred browser to:
**http://localhost:8511**

---

## 🔧 macOS-Specific Features

### Network Configuration
- ✅ **No special network setup needed** - Ollama works out of the box on macOS
- ✅ **Localhost access** - Direct connection between Python app and Ollama
- ✅ **Firewall friendly** - All communication is local

### Performance Optimization

**For Apple Silicon Macs (M1/M2/M3):**
- ✅ **Native ARM64 support** - Ollama runs natively on Apple Silicon
- ✅ **GPU acceleration** - Automatic Metal GPU acceleration
- ✅ **Memory efficiency** - Optimized for macOS memory management

**Recommended Models by Mac Type:**

| Mac Type | RAM | Recommended Model | Notes |
|----------|-----|-------------------|-------|
| **MacBook Air M1/M2** | 8GB | `llama3.2:1b` | Fast, efficient |
| **MacBook Pro M1/M2** | 16GB+ | `llama3.2:3b` | Balanced performance |
| **Mac Studio/Pro** | 32GB+ | `mistral:7b` | Best quality |

---

## 🛠️ Troubleshooting

### Common macOS Issues

**"ollama: command not found"**
```bash
# If installed via Homebrew
brew install ollama

# If using direct install, add to PATH
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**"Permission denied" when running scripts**
```bash
chmod +x scripts/*.sh
```

**Python version issues**
```bash
# Use Python 3 explicitly
python3 -m venv pdf_summarizer_env
```

**Port conflicts**
```bash
# Check what's using port 8511
lsof -i :8511

# Kill process if needed
sudo kill -9 <PID>
```

### Performance Tips

**Free up memory for better performance:**
```bash
# Check memory usage
top -o MEM

# Quit unnecessary applications before processing large PDFs
```

**Monitor Ollama performance:**
```bash
# Check Ollama status
ollama ps

# View available models
ollama list
```

---

## 🚦 Status Indicators

When everything is working correctly, you should see:

1. **Terminal 1 (Ollama):**
   ```
   time=... level=INFO source=routes.go:... msg="Listening on 127.0.0.1:11434"
   ```

2. **Terminal 2 (PDF App):**
   ```
   🚀 Starting Enhanced PDF Summarizer...
   ✅ Ollama is running and accessible!
   🌐 Starting PDF Summarizer on port 8511...
   ```

3. **Browser:**
   - Green status: "✅ Ollama is running! Models: llama3.2:3b, ..."

---

## 📱 Using the Application

### Upload Features
- **Drag & Drop** - Works perfectly in Safari/Chrome on macOS
- **Multiple Files** - Select multiple PDFs with Cmd+Click
- **File Sizes** - Up to 10MB per PDF (configurable)

### Download Features
- **PDF Downloads** - Automatically opens in Preview
- **ZIP Files** - Downloads to ~/Downloads by default
- **Combined PDFs** - Merged summaries in single document

### Keyboard Shortcuts
- **⌘+R** - Refresh page
- **⌘+T** - New tab to keep app open
- **⌘+W** - Close tab (app keeps running)

---

## 🔄 Updating

**Update Ollama:**
```bash
brew upgrade ollama  # If installed via Homebrew
# OR
curl -fsSL https://ollama.com/install.sh | sh  # Direct install
```

**Update Models:**
```bash
ollama pull llama3.2:3b  # Downloads latest version
```

**Update Python Dependencies:**
```bash
source pdf_summarizer_env/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🎯 macOS Integration

### Spotlight Search
The app folder will be indexed by Spotlight for easy access.

### Dock Integration
Pin Terminal to dock for quick access to start scripts.

### Menu Bar
Ollama may add a menu bar icon when running (depending on installation method).

### File Associations
PDFs will maintain their default Preview associations while being processed.

---

**🎉 Enjoy your enhanced PDF summarizer on macOS!**