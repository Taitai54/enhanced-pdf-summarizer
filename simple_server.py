#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import os
import PyPDF2
import requests
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
                    input[type="file"] { margin: 20px 0; }
                    button { padding: 10px 20px; font-size: 16px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>PDF Summarizer - Simple Version</h1>
                    <p>This is a simplified version to test basic functionality.</p>
                    
                    <h2>Ollama Status</h2>
                    <div id="ollama-status">Checking...</div>
                    
                    <h2>Upload PDF</h2>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <input type="file" name="pdf" accept=".pdf" required>
                        <br><br>
                        <button type="submit">Upload and Extract Text</button>
                    </form>
                    
                    <script>
                        // Check Ollama status
                        fetch('/check-ollama')
                            .then(response => response.json())
                            .then(data => {
                                const statusDiv = document.getElementById('ollama-status');
                                if (data.status === 'ok') {
                                    statusDiv.innerHTML = '<div class="status success">✅ Ollama is running! Models: ' + data.models.join(', ') + '</div>';
                                } else {
                                    statusDiv.innerHTML = '<div class="status error">❌ Ollama not available: ' + data.error + '</div>';
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
            
            # Try multiple possible Ollama locations
            ollama_urls = [
                "http://localhost:11434",
                "http://127.0.0.1:11434", 
                "http://172.24.64.1:11434"  # Windows host from WSL
            ]
            
            result = {"status": "error", "error": "Ollama not found on any host"}
            
            for url in ollama_urls:
                try:
                    response = requests.get(f"{url}/api/tags", timeout=2)
                    if response.status_code == 200:
                        models = [m['name'] for m in response.json().get('models', [])]
                        result = {"status": "ok", "models": models, "url": url}
                        break
                except Exception as e:
                    continue
            
            if result["status"] == "error":
                result["error"] = "Ollama not running. Install from https://ollama.com/download and run 'ollama serve'"
            
            self.wfile.write(json.dumps(result).encode())
        else:
            super().do_GET()

PORT = 8509
Handler = PDFHandler

print(f"Starting simple PDF server on port {PORT}")
print(f"Open your browser to: http://localhost:{PORT}")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()