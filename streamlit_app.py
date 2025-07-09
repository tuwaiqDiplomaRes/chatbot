import streamlit as st
import requests

# Streamlit setup
st.set_page_config(page_title="Gemini Stateless Chatbot", layout="centered")
st.title("🤖 Musab ")

# API config
API_KEY = st.secrets["API_key"]
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# User input
prompt = st.text_input("Ask Gemini:", placeholder="e.g., Explain how AI works...")

# Function to send a prompt to Gemini
def get_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=body)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "⚠️ Unexpected response structure."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# If user submitted a prompt
if prompt:
    with st.spinner("Gemini is thinking..."):
        answer = get_response(prompt)
    st.markdown("**Gemini says:**")
    st.markdown(answer)
