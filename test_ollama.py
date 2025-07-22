#!/usr/bin/env python3
import requests
import json

def test_ollama():
    """Test Ollama connection and generation"""
    ollama_urls = ["http://localhost:11434", "http://127.0.0.1:11434", "http://172.24.64.1:11434"]
    
    for url in ollama_urls:
        try:
            print(f"🔗 Testing Ollama URL: {url}")
            
            # Test if Ollama is running
            response = requests.get(f"{url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                print(f"✅ Ollama is running at {url}")
                print(f"📋 Available models: {models}")
                
                # Test generation
                if models:
                    model = models[0]  # Use first available model
                    print(f"🧪 Testing generation with model: {model}")
                    
                    gen_response = requests.post(f"{url}/api/generate", 
                        json={
                            "model": model,
                            "prompt": "Summarize this in one sentence: This is a test document.",
                            "stream": False
                        },
                        timeout=60
                    )
                    
                    if gen_response.status_code == 200:
                        result = gen_response.json().get('response', '')
                        print(f"✅ Generation successful: {result}")
                        return True
                    else:
                        print(f"❌ Generation failed: {gen_response.status_code}")
                        
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout connecting to {url}")
        except Exception as e:
            print(f"❌ Error with {url}: {str(e)}")
    
    print("❌ No working Ollama instance found")
    return False

if __name__ == "__main__":
    test_ollama()