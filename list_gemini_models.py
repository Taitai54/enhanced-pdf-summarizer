import google.generativeai as genai
import os

# Try to get the API key from environment or .streamlit/secrets.toml
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

if not api_key:
    print("No Gemini API key found. Please set GEMINI_API_KEY in your environment or .streamlit/secrets.toml.")
    exit(1)

genai.configure(api_key=api_key)

print("Available Gemini models and their supported generation methods:")
for m in genai.list_models():
    print(f"{m.name} | Supported methods: {m.supported_generation_methods}")
