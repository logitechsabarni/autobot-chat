import streamlit as st
import openai
import os
from PyPDF2 import PdfReader
from gtts import gTTS
import playsound
import tempfile
import speech_recognition as sr
from datetime import datetime

# -------------------------------
# OpenAI API key (from Streamlit secrets)
# -------------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🤖 AutoBot - Unified AI Assistant")

st.markdown("""
**Features included:**  
- AI Chatbot powered by GPT-4  
- PDF Upload & Contextual Answers  
- Voice Input / Output  
- Stub Functions: Email/Calendar scheduling  
""")

# -------------------------------
# PDF Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload PDF for context (optional)", type=["pdf"])
pdf_text = ""
if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()
    st.success("PDF loaded successfully!")

# -------------------------------
# Voice Input
# -------------------------------
voice_option = st.checkbox("Use voice input?")
if voice_option:
    st.write("Press 'Record' and speak")
    if st.button("Record"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening...")
            audio_data = r.listen(source, timeout=5)
            try:
                user_input = r.recognize_google(audio_data)
                st.write("You said:", user_input)
            except:
                st.write("Could not recognize voice")
                user_input = ""
else:
    user_input = st.text_input("Type your message here:")

# -------------------------------
# Send Button
# -------------------------------
if st.button("Send") and user_input.strip() != "":
    # Prepare GPT prompt
    prompt = ("You are AutoBot, an intelligent AI assistant that automates tasks, scheduling, "
              "reminders, and emails. Answer in a helpful, concise, and polite way.")
    if pdf_text:
        prompt += f" Use the following PDF context to answer: {pdf_text}"

    # Call GPT
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ]
    )
    reply = response.choices[0].message.content
    st.write("🤖 AutoBot:", reply)

    # -------------------------------
    # Voice Output
    # -------------------------------
    voice_out = st.checkbox("Read reply aloud")
    if voice_out:
        tts = gTTS(reply)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(tmp_file.name)
        playsound.playsound(tmp_file.name)

# -------------------------------
# Email Scheduling Stub
# -------------------------------
st.markdown("### 📧 Email / Calendar Automation (Demo)")
email_task = st.text_input("Type a task to schedule/send email (demo)")
if st.button("Schedule Email / Task") and email_task.strip() != "":
    # Stub function for hackathon demo
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.success(f"Task '{email_task}' scheduled successfully for {now} ✅")

# -------------------------------
# Future Enhancements Placeholder
# -------------------------------
st.markdown("""
**Future Enhancements:**  
- Connect real Google Calendar API for scheduling  
- Connect Gmail API for email automation  
- Multi-user login & personalization  
- Proactive alerts & reminders  
""")
