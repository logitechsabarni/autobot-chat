import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import date, datetime
import pandas as pd

# -----------------------------
# Function to create dummy images
# -----------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# -----------------------------
# Sidebar: User Profile & Quick Links
# -----------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
st.sidebar.write("**Tasks Completed:** 8 / 15")
st.sidebar.write("**Upcoming Tasks:** 5")
st.sidebar.write("**Next Reminder:** 2025-10-18 10:00 AM")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Quick Links")
st.sidebar.button("View Calendar")
st.sidebar.button("View Tasks")
st.sidebar.button("Payments")
st.sidebar.markdown("---")

# -----------------------------
# Main Dashboard Title
# -----------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, reminders, and payments** from a single hub!")

# -----------------------------
# Task Overview Cards
# -----------------------------
st.subheader("📊 Task Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", "8 / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", "5", "-1 from yesterday")
col3.metric("Reminders Today", "3", "+1 from yesterday")

# -----------------------------
# Initialize session state for tasks
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# Calendar / Scheduler
# -----------------------------
st.subheader("📅 Schedule Tasks")
col_date, col_task, col_button = st.columns([2, 3, 1])

with col_date:
    selected_date = st.date_input("Select a date", value=date.today())
with col_task:
    task_name = st.text_input("Enter task name")
with col_button:
    if st.button("Schedule Task"):
        if task_name.strip() != "":
            st.session_state.tasks.append({"date": selected_date, "task": task_name})
            st.success(f"Task '{task_name}' scheduled on {selected_date}!")
        else:
            st.warning("Please enter a task name!")

# -----------------------------
# Display all scheduled tasks
# -----------------------------
st.subheader("📝 Scheduled Tasks")
if st.session_state.tasks:
    df_tasks = pd.DataFrame(st.session_state.tasks)
    df_tasks["date"] = pd.to_datetime(df_tasks["date"]).dt.date
    st.dataframe(df_tasks)
else:
    st.info("No tasks scheduled yet.")

# -----------------------------
# Dummy notifications for today's tasks
# -----------------------------
st.subheader("🔔 Notifications")
today = date.today()
tasks_today = [t["task"] for t in st.session_state.tasks if t["date"] == today]
if tasks_today:
    for t in tasks_today:
        st.info(f"Reminder: Today you have '{t}'!")
else:
    st.write("No notifications for today.")

# -----------------------------
# Dummy Chat with AutoBot
# -----------------------------
st.subheader("💬 Chat with AutoBot (Dummy Responses)")
dummy_responses = [
    "Don't forget your meeting at 5 PM today!",
    "You have 3 upcoming tasks this week.",
    "Reminder: Pay your electricity bill on time.",
    "Great job completing your tasks!",
    "Try to finish your pending reports today.",
    "Your next appointment is on 2025-10-19.",
    "Don't forget to review your emails.",
    "Keep up the productivity! 💪",
    "You have a new task to add: 'Prepare presentation'.",
    "Check your calendar for upcoming deadlines.",
    "Have you completed your weekly review?",
    "It's a good day to plan your tasks.",
    "Reminder: Team meeting tomorrow at 3 PM.",
    "Schedule your breaks to stay productive.",
    "Your tasks are on track for this week.",
    "Don't forget to update your progress.",
    "New task suggestion: 'Read AI research papers'.",
    "Stay focused and avoid distractions.",
    "Next reminder: 2025-10-20 09:00 AM",
    "You've completed 8 tasks this week. Awesome!"
]

user_input = st.text_input("Type your message here")
if st.button("Send Message"):
    if user_input.strip() != "":
        response = random.choice(dummy_responses)
        st.markdown(f"**AutoBot:** {response}")
        # Optionally, append chat to session_state for history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history.append({"user": user_input, "bot": response})

# Display chat history
if "chat_history" in st.session_state:
    for chat in st.session_state.chat_history[-5:]:  # Show last 5 messages
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**AutoBot:** {chat['bot']}")

# -----------------------------
# Dummy Payment Section
# -----------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
st.write("Upcoming payments (dummy data):")
payments = [
    {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
    {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
    {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"},
]
for p in payments:
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")
