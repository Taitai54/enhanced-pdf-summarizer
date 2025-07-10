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
import io
from pathlib import Path

class PDFHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>PDF Summarizer</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
                    .success { background-color: #d4edda; color: #155724; }
                    .error { background-color: #f8d7da; color: #721c24; }
                    .warning { background-color: #fff3cd; color: #856404; }
                    input[type="file"] { margin: 10px 0; }
                    textarea { width: 100%; height: 100px; margin: 10px 0; }
                    button { padding: 10px 20px; font-size: 16px; margin: 10px 0; }
                    #result { margin-top: 20px; padding: 20px; border: 1px solid #ddd; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>PDF Summarizer</h1>
                    
                    <h2>Ollama Status</h2>
                    <div id="ollama-status">Checking...</div>
                    
                    <h2>Summarize PDF</h2>
                    <form id="pdf-form">
                        <div>
                            <label>Select PDF file:</label><br>
                            <input type="file" id="pdf-file" accept=".pdf" required>
                        </div>
                        
                        <div>
                            <label>Custom prompt (optional):</label><br>
                            <textarea id="custom-prompt" placeholder="Enter custom instructions here, e.g., 'Summarize this in bullet points' or 'Extract key findings'"></textarea>
                        </div>
                        
                        <div>
                            <label>Summary length:</label><br>
                            <select id="summary-length">
                                <option value="short">Short (200-300 words)</option>
                                <option value="medium" selected>Medium (400-600 words)</option>
                                <option value="long">Long (800-1000 words)</option>
                            </select>
                        </div>
                        
                        <button type="submit">Summarize PDF</button>
                    </form>
                    
                    <div id="result"></div>
                    
                    <script>
                        // Check Ollama status
                        fetch('/check-ollama')
                            .then(response => response.json())
                            .then(data => {
                                const statusDiv = document.getElementById('ollama-status');
                                if (data.status === 'ok') {
                                    statusDiv.innerHTML = '<div class="status success">✅ Ollama is running! Models: ' + data.models.join(', ') + '</div>';
                                } else {
                                    statusDiv.innerHTML = '<div class="status error">❌ ' + data.error + '</div>';
                                }
                            });
                        
                        // Handle form submission
                        document.getElementById('pdf-form').addEventListener('submit', async function(e) {
                            e.preventDefault();
                            
                            const fileInput = document.getElementById('pdf-file');
                            const customPrompt = document.getElementById('custom-prompt').value;
                            const summaryLength = document.getElementById('summary-length').value;
                            const resultDiv = document.getElementById('result');
                            
                            if (!fileInput.files[0]) {
                                alert('Please select a PDF file');
                                return;
                            }
                            
                            const formData = new FormData();
                            formData.append('pdf', fileInput.files[0]);
                            formData.append('prompt', customPrompt);
                            formData.append('length', summaryLength);
                            
                            resultDiv.innerHTML = '<div class="status warning">Processing PDF... This may take a few minutes.</div>';
                            
                            try {
                                const response = await fetch('/summarize', {
                                    method: 'POST',
                                    body: formData
                                });
                                
                                const data = await response.json();
                                
                                if (data.status === 'success') {
                                    resultDiv.innerHTML = '<div class="status success">✅ Summary completed!</div><h3>Summary:</h3><div style="white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 5px;">' + data.summary + '</div>';
                                } else {
                                    resultDiv.innerHTML = '<div class="status error">❌ Error: ' + data.error + '</div>';
                                }
                            } catch (error) {
                                resultDiv.innerHTML = '<div class="status error">❌ Error: ' + error.message + '</div>';
                            }
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
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/summarize':
            try:
                # Parse the form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Get the uploaded file
                pdf_file = form['pdf']
                custom_prompt = form.getvalue('prompt', '')
                summary_length = form.getvalue('length', 'medium')
                
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
                
                # Create summary prompt
                length_instructions = {
                    'short': 'in 200-300 words',
                    'medium': 'in 400-600 words', 
                    'long': 'in 800-1000 words'
                }
                
                if custom_prompt:
                    prompt = f"{custom_prompt}\n\nText to process:\n{text}"
                else:
                    prompt = f"Please provide a comprehensive summary of the following text {length_instructions[summary_length]}:\n\n{text}"
                
                # Send to Ollama
                ollama_urls = ["http://localhost:11434", "http://127.0.0.1:11434", "http://172.24.64.1:11434"]
                
                for url in ollama_urls:
                    try:
                        response = requests.post(f"{url}/api/generate", 
                            json={
                                "model": "llama3.2:3b",
                                "prompt": prompt,
                                "stream": False
                            },
                            timeout=300
                        )
                        
                        if response.status_code == 200:
                            summary = response.json().get('response', 'No response generated')
                            self.send_json_response({"status": "success", "summary": summary})
                            return
                    except Exception as e:
                        continue
                
                self.send_error_response("Could not connect to Ollama")
                
            except Exception as e:
                self.send_error_response(f"Error processing PDF: {str(e)}")
        else:
            self.send_error(404)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_error_response(self, message):
        self.send_json_response({"status": "error", "error": message})

PORT = 8510
Handler = PDFHandler

print(f"Starting PDF Summarizer on port {PORT}")
print(f"Open your browser to: http://localhost:{PORT}")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()