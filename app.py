import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime

# --------------------------
# Function to create dummy images
# --------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

# Create all images in-memory
user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# --------------------------
# Sidebar: User Profile
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
st.sidebar.write("**Tasks Completed:** 8 / 15")
st.sidebar.write("**Upcoming Tasks:** 5")
st.sidebar.write("**Next Reminder:** 2025-10-18 10:00 AM")
st.sidebar.markdown("---")

# --------------------------
# Sidebar: Quick Links
# --------------------------
st.sidebar.markdown("### 📌 Quick Links")
if st.sidebar.button("View Calendar"):
    st.sidebar.info("Calendar section is visible in the main dashboard below.")
if st.sidebar.button("View Tasks"):
    st.sidebar.info("Task management section is visible below.")
if st.sidebar.button("Payments"):
    st.sidebar.info("Payments section is visible below.")
st.sidebar.markdown("---")

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, and reminders** from a single hub!")

# --------------------------
# Task Overview Cards
# --------------------------
st.subheader("📊 Task Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", "8 / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", "5", "-1 from yesterday")
col3.metric("Reminders Today", "3", "+1 from yesterday")

# --------------------------
# Calendar Section
# --------------------------
st.subheader("📅 Calendar & Task Scheduling")
dates = ["2025-10-18", "2025-10-19", "2025-10-20"]
tasks_on_date = {
    "2025-10-18": ["Pay electricity bill", "Team meeting 5 PM"],
    "2025-10-19": ["Doctor appointment", "Submit report"],
    "2025-10-20": ["Buy groceries", "Gym session"],
}

selected_date = st.selectbox("Select a date to view/add tasks", dates)
st.write("### Tasks for", selected_date)
for task in tasks_on_date[selected_date]:
    st.checkbox(task)

new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if new_task.strip() != "":
        tasks_on_date[selected_date].append(new_task)
        st.success(f"Task '{new_task}' added to {selected_date}!")
    else:
        st.warning("Please enter a task before adding.")

# --------------------------
# Dummy Chat Section
# --------------------------
st.subheader("💬 Chat with AutoBot (Dummy Responses)")
dummy_responses = [
    "Hello! I'm AutoBot, your AI assistant 🤖",
    "Hi there! How can I assist you today?",
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
    "You've completed 8 tasks this week. Awesome!",
    "You have pending payments: Electricity Bill, Internet Bill.",
    "Your next reminder is set for tomorrow at 10 AM.",
    "I can help you schedule meetings and reminders efficiently.",
    "Want me to summarize your tasks for the week?",
    "Reminder: Your internet bill is due on 2025-10-20.",
    "You have 5 tasks remaining for this week.",
    "Consider prioritizing your most important tasks first.",
    "Don't forget to mark your completed payments and tasks.",
]

user_input = st.text_input("Type your message")
if st.button("Send Message"):
    response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {response}")

# --------------------------
# Payment Section
# --------------------------
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
    if st.button(f"Mark {p['name']} as Paid"):
        st.success(f"{p['name']} marked as paid! ✅")
