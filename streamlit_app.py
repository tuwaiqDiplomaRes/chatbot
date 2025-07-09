import streamlit as st
import requests
import json

# Streamlit page settings
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini 2.0 Flash Chatbot")

# Load API key from Streamlit secrets
API_KEY = st.secrets["API_key"]
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("You:", placeholder="Ask me anything about AI...", key="user_input")

# Function to send request to Gemini
def generate_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()
        try:
            return content["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "⚠️ Unexpected response structure."
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# If user enters a message
if user_input:
    st.session_state.chat_history.append(("🧑", user_input))
    with st.spinner("Gemini is thinking..."):
        reply = generate_response(user_input)
    st.session_state.chat_history.append(("🤖", reply))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}**: {message}")
