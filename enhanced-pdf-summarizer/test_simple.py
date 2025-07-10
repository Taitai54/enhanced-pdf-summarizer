import streamlit as st
import requests

st.title("Simple Test App")

# Test basic functionality
st.write("Testing basic Streamlit functionality...")

# Test Ollama connection
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        st.success("✅ Ollama is running and accessible!")
        models = response.json().get('models', [])
        if models:
            st.write(f"Available models: {[m['name'] for m in models]}")
        else:
            st.warning("No models found. Run: ollama pull llama3.2:3b")
    else:
        st.error("❌ Ollama is not responding properly")
except requests.RequestException as e:
    st.error(f"❌ Cannot connect to Ollama: {e}")
    st.write("Make sure Ollama is installed and running on Windows")

st.write("If you see this message, Streamlit is working!")