#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import os
import PyPDF2
import requests
try:
    import cgi
except ImportError:
    # For Python 3.11+ compatibility
    import email.message
    import email.parser
    import io
    import urllib.parse
    
    # Create a minimal cgi replacement
    class FieldStorage:
        def __init__(self, fp, headers, environ):
            self._fields = {}
            if headers.get('content-type', '').startswith('multipart/form-data'):
                boundary = headers.get('content-type').split('boundary=')[1].strip()
                data = fp.read()
                self._parse_multipart(data, boundary)
        
        def _parse_multipart(self, data, boundary):
            parts = data.split(f'--{boundary}'.encode())
            for part in parts[1:-1]:  # Skip first empty and last closing parts
                if b'\r\n\r\n' in part:
                    header_data, content = part.split(b'\r\n\r\n', 1)
                    headers = header_data.decode().strip()
                    if 'name="' in headers:
                        name = headers.split('name="')[1].split('"')[0]
                        if 'filename="' in headers:
                            filename = headers.split('filename="')[1].split('"')[0]
                            self._fields[name] = type('FileField', (), {
                                'filename': filename,
                                'file': io.BytesIO(content.rstrip(b'\r\n'))
                            })()
                        else:
                            self._fields[name] = content.decode().rstrip('\r\n')
        
        def __getitem__(self, key):
            return self._fields[key]
        
        def getvalue(self, key, default=None):
            return self._fields.get(key, default)
    
    cgi = type('CGI', (), {'FieldStorage': FieldStorage})()
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class EnhancedPDFHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Enhanced PDF Summarizer</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 1000px; margin: 0 auto; }
                    .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .success { background-color: #d4edda; color: #155724; }
                    .error { background-color: #f8d7da; color: #721c24; }
                    .warning { background-color: #fff3cd; color: #856404; }
                    .info { background-color: #d1ecf1; color: #0c5460; }
                    input[type="file"] { margin: 10px 0; }
                    textarea { width: 100%; height: 120px; margin: 10px 0; font-family: monospace; }
                    select, input[type="number"] { margin: 10px 0; padding: 5px; }
                    button { padding: 12px 24px; font-size: 16px; margin: 10px 5px; cursor: pointer; }
                    .primary-btn { background-color: #007bff; color: white; border: none; border-radius: 4px; }
                    .secondary-btn { background-color: #6c757d; color: white; border: none; border-radius: 4px; }
                    .download-btn { background-color: #28a745; color: white; border: none; border-radius: 4px; }
                    #result { margin-top: 20px; }
                    .summary-item { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
                    .summary-header { font-weight: bold; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
                    .summary-content { white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 5px; font-size: 14px; line-height: 1.5; }
                    .progress-bar { width: 100%; height: 20px; background-color: #e9ecef; border-radius: 10px; overflow: hidden; margin: 10px 0; }
                    .progress-fill { height: 100%; background-color: #007bff; transition: width 0.3s ease; }
                    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
                    .form-group { margin: 15px 0; }
                    .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
                    .file-info { background: #f8f9fa; padding: 10px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Enhanced PDF Summarizer</h1>
                    <p>Batch process multiple PDFs with custom summaries and download options.</p>
                    
                    <h2>Ollama Status</h2>
                    <div id="ollama-status">Checking...</div>
                    
                    <h2>PDF Processing</h2>
                    <form id="pdf-form">
                        <div class="form-group">
                            <label>Select PDF files (multiple files supported):</label>
                            <input type="file" id="pdf-files" accept=".pdf" multiple required>
                            <div id="file-info" class="file-info" style="display: none;"></div>
                        </div>
                        
                        <div class="grid">
                            <div>
                                <div class="form-group">
                                    <label>Summary length:</label>
                                    <select id="summary-length">
                                        <option value="short">Short (200-300 words)</option>
                                        <option value="medium" selected>Medium (500-700 words)</option>
                                        <option value="long">Long (1000-1500 words)</option>
                                        <option value="very-long">Very Long (2000+ words)</option>
                                        <option value="custom">Custom length</option>
                                    </select>
                                </div>
                                
                                <div class="form-group" id="custom-length-group" style="display: none;">
                                    <label>Custom word count:</label>
                                    <input type="number" id="custom-word-count" min="100" max="5000" value="800">
                                </div>
                                
                                <div class="form-group">
                                    <label>AI Model:</label>
                                    <select id="ai-model" disabled>
                                        <option value="">Loading models...</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label>Output format:</label>
                                    <select id="output-format">
                                        <option value="text">Text only</option>
                                        <option value="pdf" selected>PDF document</option>
                                        <option value="both">Both (text + PDF)</option>
                                    </select>
                                </div>
                            </div>
                            
                            <div>
                                <div class="form-group">
                                    <label>Summary style:</label>
                                    <select id="summary-style">
                                        <option value="comprehensive">Comprehensive overview</option>
                                        <option value="bullet-points">Bullet points</option>
                                        <option value="executive">Executive summary</option>
                                        <option value="technical">Technical analysis</option>
                                        <option value="key-findings">Key findings only</option>
                                        <option value="custom">Custom instructions</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label>Batch processing:</label>
                                    <select id="batch-mode">
                                        <option value="individual">Individual summaries</option>
                                        <option value="combined">Combined summary</option>
                                        <option value="comparison">Comparison analysis</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Custom instructions (optional):</label>
                            <textarea id="custom-prompt" placeholder="Enter specific instructions like:
- Focus on financial data
- Extract methodology sections
- Summarize conclusions and recommendations
- Compare findings across documents
- Highlight key statistics"></textarea>
                        </div>
                        
                        <button type="submit" class="primary-btn">Process PDF(s)</button>
                        <button type="button" id="clear-results" class="secondary-btn">Clear Results</button>
                    </form>
                    
                    <div id="progress-container" style="display: none;">
                        <h3>Processing Progress</h3>
                        <div class="progress-bar">
                            <div id="progress-fill" class="progress-fill" style="width: 0%"></div>
                        </div>
                        <div id="progress-text">Starting...</div>
                    </div>
                    
                    <div id="result"></div>
                    
                    <script>
                        let processedSummaries = [];
                        
                        // Check Ollama status and populate model dropdown
                        fetch('/check-ollama')
                            .then(response => response.json())
                            .then(data => {
                                const statusDiv = document.getElementById('ollama-status');
                                const modelSelect = document.getElementById('ai-model');
                                
                                if (data.status === 'ok') {
                                    statusDiv.innerHTML = '<div class="status success">✅ Ollama is running! Models: ' + data.models.join(', ') + '</div>';
                                    
                                    // Populate model dropdown
                                    modelSelect.innerHTML = '';
                                    data.models.forEach(model => {
                                        const option = document.createElement('option');
                                        option.value = model;
                                        option.textContent = model;
                                        // Set default to llama3.2:3b if available
                                        if (model === 'llama3.2:3b') {
                                            option.selected = true;
                                        }
                                        modelSelect.appendChild(option);
                                    });
                                    
                                    // Enable model selection
                                    modelSelect.disabled = false;
                                } else {
                                    statusDiv.innerHTML = '<div class="status error">❌ ' + data.error + '</div>';
                                    modelSelect.disabled = true;
                                }
                            });
                        
                        // Handle file selection
                        document.getElementById('pdf-files').addEventListener('change', function(e) {
                            const files = e.target.files;
                            const fileInfo = document.getElementById('file-info');
                            
                            if (files.length > 0) {
                                let info = `<strong>Selected files (${files.length}):</strong><br>`;
                                for (let i = 0; i < files.length; i++) {
                                    const size = (files[i].size / 1024 / 1024).toFixed(2);
                                    info += `• ${files[i].name} (${size} MB)<br>`;
                                }
                                fileInfo.innerHTML = info;
                                fileInfo.style.display = 'block';
                            } else {
                                fileInfo.style.display = 'none';
                            }
                        });
                        
                        // Handle summary length change
                        document.getElementById('summary-length').addEventListener('change', function(e) {
                            const customGroup = document.getElementById('custom-length-group');
                            if (e.target.value === 'custom') {
                                customGroup.style.display = 'block';
                            } else {
                                customGroup.style.display = 'none';
                            }
                        });
                        
                        // Handle form submission
                        document.getElementById('pdf-form').addEventListener('submit', async function(e) {
                            e.preventDefault();
                            
                            const fileInput = document.getElementById('pdf-files');
                            const files = fileInput.files;
                            
                            if (files.length === 0) {
                                alert('Please select at least one PDF file');
                                return;
                            }
                            
                            processedSummaries = [];
                            showProgress(true);
                            
                            const resultDiv = document.getElementById('result');
                            resultDiv.innerHTML = '';
                            
                            for (let i = 0; i < files.length; i++) {
                                await processSingleFile(files[i], i + 1, files.length);
                            }
                            
                            showProgress(false);
                            showDownloadOptions();
                        });
                        
                        async function processSingleFile(file, index, total) {
                            updateProgress(((index - 1) / total) * 100, `Processing ${file.name}...`);
                            
                            const formData = new FormData();
                            formData.append('pdf', file);
                            formData.append('prompt', document.getElementById('custom-prompt').value);
                            formData.append('length', document.getElementById('summary-length').value);
                            formData.append('custom-word-count', document.getElementById('custom-word-count').value);
                            formData.append('style', document.getElementById('summary-style').value);
                            formData.append('output-format', document.getElementById('output-format').value);
                            formData.append('batch-mode', document.getElementById('batch-mode').value);
                            formData.append('ai-model', document.getElementById('ai-model').value);
                            
                            try {
                                const response = await fetch('/summarize', {
                                    method: 'POST',
                                    body: formData
                                });
                                
                                const data = await response.json();
                                
                                if (data.status === 'success') {
                                    processedSummaries.push({
                                        filename: file.name,
                                        summary: data.summary,
                                        downloadUrl: data.download_url
                                    });
                                    
                                    displaySummary(file.name, data.summary, data.download_url);
                                } else {
                                    displayError(file.name, data.error);
                                }
                            } catch (error) {
                                displayError(file.name, error.message);
                            }
                            
                            updateProgress((index / total) * 100, `Completed ${index} of ${total} files`);
                        }
                        
                        function displaySummary(filename, summary, downloadUrl) {
                            const resultDiv = document.getElementById('result');
                            const summaryDiv = document.createElement('div');
                            summaryDiv.className = 'summary-item';
                            
                            let downloadButton = '';
                            if (downloadUrl) {
                                downloadButton = `<button onclick="downloadFile('${downloadUrl}', '${filename}')" class="download-btn">Download PDF</button>`;
                            }
                            
                            summaryDiv.innerHTML = `
                                <div class="summary-header">
                                    📄 ${filename}
                                    ${downloadButton}
                                </div>
                                <div class="summary-content">${summary}</div>
                            `;
                            
                            resultDiv.appendChild(summaryDiv);
                        }
                        
                        function displayError(filename, error) {
                            const resultDiv = document.getElementById('result');
                            const errorDiv = document.createElement('div');
                            errorDiv.className = 'summary-item';
                            errorDiv.innerHTML = `
                                <div class="summary-header">❌ ${filename}</div>
                                <div class="status error">Error: ${error}</div>
                            `;
                            resultDiv.appendChild(errorDiv);
                        }
                        
                        function showProgress(show) {
                            const progressContainer = document.getElementById('progress-container');
                            progressContainer.style.display = show ? 'block' : 'none';
                        }
                        
                        function updateProgress(percent, text) {
                            const progressFill = document.getElementById('progress-fill');
                            const progressText = document.getElementById('progress-text');
                            
                            progressFill.style.width = percent + '%';
                            progressText.textContent = text;
                        }
                        
                        function showDownloadOptions() {
                            if (processedSummaries.length > 1) {
                                const resultDiv = document.getElementById('result');
                                const downloadDiv = document.createElement('div');
                                downloadDiv.className = 'summary-item';
                                downloadDiv.innerHTML = `
                                    <div class="summary-header">📦 Batch Download Options</div>
                                    <button onclick="downloadAllSummaries()" class="download-btn">Download All Summaries (ZIP)</button>
                                    <button onclick="downloadBatchSummary()" class="download-btn">Download Combined Summary</button>
                                `;
                                resultDiv.insertBefore(downloadDiv, resultDiv.firstChild);
                            }
                        }
                        
                        function downloadFile(url, filename) {
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = filename.replace('.pdf', '_summary.pdf');
                            a.click();
                        }
                        
                        function downloadAllSummaries() {
                            fetch('/download-batch', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ summaries: processedSummaries })
                            })
                            .then(response => response.blob())
                            .then(blob => {
                                const url = window.URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'all_summaries.zip';
                                a.click();
                                window.URL.revokeObjectURL(url);
                            });
                        }
                        
                        function downloadBatchSummary() {
                            const combined = processedSummaries.map(s => 
                                `=== ${s.filename} ===\\n\\n${s.summary}\\n\\n`
                            ).join('\\n');
                            
                            fetch('/create-combined-pdf', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ content: combined })
                            })
                            .then(response => response.blob())
                            .then(blob => {
                                const url = window.URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'combined_summary.pdf';
                                a.click();
                                window.URL.revokeObjectURL(url);
                            });
                        }
                        
                        // Clear results
                        document.getElementById('clear-results').addEventListener('click', function() {
                            document.getElementById('result').innerHTML = '';
                            processedSummaries = [];
                        });
                    </script>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/check-ollama':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            ollama_urls = [
                "http://localhost:11434",
                "http://127.0.0.1:11434", 
                "http://172.24.64.1:11434"
            ]
            
            result = {"status": "error", "error": "Ollama not found"}
            
            for url in ollama_urls:
                try:
                    response = requests.get(f"{url}/api/tags", timeout=2)
                    if response.status_code == 200:
                        models = [m['name'] for m in response.json().get('models', [])]
                        result = {"status": "ok", "models": models, "url": url}
                        break
                except Exception:
                    continue
            
            self.wfile.write(json.dumps(result).encode())
            
        elif self.path.startswith('/download/'):
            # Handle file downloads
            filename = self.path[10:]  # Remove '/download/'
            filepath = os.path.join(tempfile.gettempdir(), filename)
            
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'application/pdf')
                self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                self.end_headers()
                
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/summarize':
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                pdf_file = form['pdf']
                custom_prompt = form.getvalue('prompt', '')
                summary_length = form.getvalue('length', 'medium')
                custom_word_count = form.getvalue('custom-word-count', '800')
                summary_style = form.getvalue('style', 'comprehensive')
                output_format = form.getvalue('output-format', 'text')
                batch_mode = form.getvalue('batch-mode', 'individual')
                ai_model = form.getvalue('ai-model', 'llama3.2:3b')
                
                if not pdf_file.filename:
                    self.send_error_response("No file uploaded")
                    return
                
                # Extract text from PDF
                pdf_data = pdf_file.file.read()
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                if not text.strip():
                    self.send_error_response("No text found in PDF")
                    return
                
                # Create enhanced summary prompt
                prompt = self.create_enhanced_prompt(text, custom_prompt, summary_length, 
                                                  custom_word_count, summary_style)
                
                # Send to Ollama
                summary = self.generate_summary(prompt, ai_model)
                if not summary:
                    self.send_error_response("Could not generate summary")
                    return
                
                # Create downloadable file if requested
                download_url = None
                if output_format in ['pdf', 'both']:
                    download_url = self.create_pdf_summary(pdf_file.filename, summary)
                
                self.send_json_response({
                    "status": "success", 
                    "summary": summary,
                    "download_url": download_url
                })
                
            except Exception as e:
                self.send_error_response(f"Error processing PDF: {str(e)}")
                
        elif self.path == '/download-batch':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Create ZIP file with all summaries
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for i, summary_data in enumerate(data['summaries']):
                        filename = f"{summary_data['filename']}_summary.txt"
                        zip_file.writestr(filename, summary_data['summary'])
                
                zip_buffer.seek(0)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/zip')
                self.send_header('Content-Disposition', 'attachment; filename="all_summaries.zip"')
                self.end_headers()
                self.wfile.write(zip_buffer.getvalue())
                
            except Exception as e:
                self.send_error_response(f"Error creating batch download: {str(e)}")
                
        elif self.path == '/create-combined-pdf':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Create combined PDF
                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=16,
                    spaceAfter=30,
                    alignment=1  # Center alignment
                )
                story.append(Paragraph("Combined PDF Summaries", title_style))
                story.append(Spacer(1, 20))
                
                # Add content
                content_style = ParagraphStyle(
                    'CustomContent',
                    parent=styles['Normal'],
                    fontSize=10,
                    spaceAfter=12,
                    leftIndent=20
                )
                
                for line in data['content'].split('\n'):
                    if line.strip():
                        story.append(Paragraph(line, content_style))
                    else:
                        story.append(Spacer(1, 6))
                
                doc.build(story)
                pdf_buffer.seek(0)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/pdf')
                self.send_header('Content-Disposition', 'attachment; filename="combined_summary.pdf"')
                self.end_headers()
                self.wfile.write(pdf_buffer.getvalue())
                
            except Exception as e:
                self.send_error_response(f"Error creating combined PDF: {str(e)}")
        else:
            self.send_error(404)

    def create_enhanced_prompt(self, text, custom_prompt, length, custom_word_count, style):
        """Create an enhanced prompt based on user preferences"""
        
        # Word count mapping
        word_counts = {
            'short': '200-300 words',
            'medium': '500-700 words',
            'long': '1000-1500 words',
            'very-long': '2000+ words',
            'custom': f'{custom_word_count} words'
        }
        
        # Style templates
        style_instructions = {
            'comprehensive': 'Provide a comprehensive overview covering all major points',
            'bullet-points': 'Structure your response as clear bullet points with key information',
            'executive': 'Write an executive summary focusing on key decisions and outcomes',
            'technical': 'Focus on technical details, methodologies, and specifications',
            'key-findings': 'Extract and highlight only the most important findings and conclusions',
            'custom': ''
        }
        
        word_limit = word_counts.get(length, '500-700 words')
        style_instruction = style_instructions.get(style, '')
        
        if custom_prompt:
            prompt = f"{custom_prompt}\n\n{style_instruction}\n\nPlease limit your response to {word_limit}.\n\nText to process:\n{text}"
        else:
            prompt = f"{style_instruction}\n\nPlease provide a summary in {word_limit} of the following text:\n\n{text}"
        
        return prompt

    def generate_summary(self, prompt, model="llama3.2:3b"):
        """Generate summary using Ollama with specified model"""
        ollama_urls = ["http://localhost:11434", "http://127.0.0.1:11434", "http://172.24.64.1:11434"]
        
        for url in ollama_urls:
            try:
                response = requests.post(f"{url}/api/generate", 
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=300
                )
                
                if response.status_code == 200:
                    return response.json().get('response', '')
            except Exception:
                continue
        
        return None

    def create_pdf_summary(self, original_filename, summary):
        """Create a downloadable PDF summary"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"{original_filename}_{timestamp}_summary.pdf"
            pdf_path = os.path.join(tempfile.gettempdir(), pdf_filename)
            
            # Create PDF
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=14,
                spaceAfter=30
            )
            story.append(Paragraph(f"Summary of {original_filename}", title_style))
            story.append(Spacer(1, 20))
            
            # Add timestamp
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor='gray'
            )
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
            story.append(Spacer(1, 20))
            
            # Add summary content
            content_style = ParagraphStyle(
                'CustomContent',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                leftIndent=20
            )
            
            for paragraph in summary.split('\n\n'):
                if paragraph.strip():
                    story.append(Paragraph(paragraph, content_style))
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            
            return f"/download/{pdf_filename}"
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return None

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, message):
        self.send_json_response({"status": "error", "error": message})

PORT = 8511
Handler = EnhancedPDFHandler

print(f"Starting Enhanced PDF Summarizer on port {PORT}")
print(f"Open your browser to: http://localhost:{PORT}")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()