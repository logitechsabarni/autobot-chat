import streamlit as st
from openai import OpenAI

# -----------------------------
# Initialize OpenAI client
# -----------------------------
# Make sure your OPENAI_API_KEY is added in Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(page_title="🤖 AutoBot Chat Assistant", page_icon="💬")

# -----------------------------
# App title and description
# -----------------------------
st.title("🤖 AutoBot Chat Assistant")
st.write(
    "Welcome! I'm AutoBot — your AI-powered assistant ready to help you automate tasks, schedule events, and manage reminders!"
)

# -----------------------------
# Sidebar info and tips
# -----------------------------
with st.sidebar:
    st.header("⚙️ App Settings")
    st.write("Built using **Streamlit** and **OpenAI GPT-4 Turbo**.")
    st.markdown("---")
    st.write("💡 Tip: Try asking me things like:")
    st.markdown("""
    - "Schedule a meeting with John at 5 PM tomorrow"
    - "Remind me to pay my electricity bill on Monday"
    - "Summarize my tasks for the week"
    """)
    st.markdown("---")
    st.write("Made by **Sabarni Guha** 🔥")
    st.info("⚠️ AutoBot may be temporarily unavailable if API limits are reached.")

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are AutoBot, an intelligent assistant that helps users with task automation, scheduling, and reminders."}
    ]

# -----------------------------
# Predefined fallback responses
# -----------------------------
fallback_cache = {
    "hi": "Hello! I’m AutoBot, your AI assistant 🤖",
    "hello": "Hi there! How can I help you today?",
    "help": "I can help you schedule meetings, set reminders, manage tasks, and more!"
}

# -----------------------------
# Display previous chat messages
# -----------------------------
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Type your message here...")

# -----------------------------
# Handle user input
# -----------------------------
if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # -----------------------------
    # Check fallback cache first
    # -----------------------------
    user_input_lower = user_input.lower()
    if user_input_lower in fallback_cache:
        reply = fallback_cache[user_input_lower]
    else:
        # -----------------------------
        # Call OpenAI API safely
        # -----------------------------
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = "🤖 Sorry, I’m temporarily unavailable due to API limits. Please try again later!"

    # Display assistant message
    st.chat_message("assistant").markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
