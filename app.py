import streamlit as st
import openai
import PyPDF2
import requests
import io
import pyttsx3
from gtts import gTTS
import speech_recognition as sr

# -------------------------
# 🔑 OpenAI API Key
# -------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store your key in Streamlit Secrets

# -------------------------
# Streamlit UI
# -------------------------
st.title("🤖 AutoBot - Your Unified AI Assistant")

st.sidebar.header("Upload Files or Speak")
uploaded_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
voice_input = st.sidebar.button("Speak")

# Text input
user_input = st.text_input("Type your message to AutoBot:")

# -------------------------
# Function: OpenAI Chat
# -------------------------
def chat_with_autobot(message):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are AutoBot, an intelligent personal assistant that automates scheduling, reminders, payments, and more."},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message["content"]

# -------------------------
# Function: Read PDF
# -------------------------
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# -------------------------
# Function: TTS
# -------------------------
def speak_text(text):
    try:
        # Use pyttsx3 (offline)
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        # Fallback: gTTS (online)
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        st.audio("output.mp3")

# -------------------------
# Function: Speech Recognition
# -------------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        return recognizer.recognize_google(audio)
    except:
        return ""

# -------------------------
# Handle Voice Input
# -------------------------
if voice_input:
    user_input = get_voice_input()
    st.write(f"🎙 You said: {user_input}")

# -------------------------
# Handle PDF Input
# -------------------------
if uploaded_file:
    pdf_text = read_pdf(uploaded_file)
    st.text_area("PDF Content", pdf_text, height=200)
    user_input += "\n" + pdf_text  # Append PDF content to message

# -------------------------
# Handle Chat Submission
# -------------------------
if st.button("Send") and user_input:
    reply = chat_with_autobot(user_input)
    st.write(f"🤖 AutoBot: {reply}")
    speak_text(reply)
