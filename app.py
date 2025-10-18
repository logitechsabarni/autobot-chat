import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime, timedelta
import time

# --------------------------
# Function to create dummy images
# --------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

# --------------------------
# Create dummy images
# --------------------------
user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")
reminder_img = create_dummy_image((150, 255, 150), text="Rem")

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# --------------------------
# Initialize session state
# --------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "2025-10-18": ["Pay electricity bill", "Team meeting 5 PM"],
        "2025-10-19": ["Doctor appointment", "Submit report"],
        "2025-10-20": ["Buy groceries", "Gym session"],
    }

if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"},
    ]

if "dummy_responses" not in st.session_state:
    st.session_state.dummy_responses = [
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
        "Prepare for tomorrow's client call.",
        "Remember to submit your report before noon.",
        "Your subscription will expire soon.",
        "Check your emails for urgent messages.",
        "Time to hydrate and take a break!",
        "Your meeting has been rescheduled.",
        "New task added: 'Review project proposal'.",
        "Remember to backup your files.",
        "Plan your weekend tasks today.",
        "Don't forget your fitness session tonight."
    ]

# --------------------------
# Sidebar: User Profile
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
completed_tasks = sum([len(v) for v in st.session_state.tasks.values()]) - 5  # dummy metric
st.sidebar.write(f"**Tasks Completed:** {completed_tasks} / 15")
upcoming_tasks = 5  # dummy
st.sidebar.write(f"**Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write("**Next Reminder:** 2025-10-18 10:00 AM")
st.sidebar.markdown("---")

# --------------------------
# Sidebar: Quick Links
# --------------------------
st.sidebar.markdown("### 📌 Quick Links")
st.sidebar.button("View Calendar")
st.sidebar.button("View Tasks")
st.sidebar.button("Payments")
st.sidebar.button("View Reminders")
st.sidebar.markdown("---")

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, reminders, and payments** from a single hub!")

# --------------------------
# Task Overview Cards
# --------------------------
st.subheader("📊 Task Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{completed_tasks} / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", f"{upcoming_tasks}", "-1 from yesterday")
col3.metric("Reminders Today", "3", "+1 from yesterday")

# --------------------------
# Calendar Section
# --------------------------
st.subheader("📅 Calendar")
dates = list(st.session_state.tasks.keys())
selected_date = st.selectbox("Select a date", dates)
st.write("### Tasks for", selected_date)
for task in st.session_state.tasks[selected_date]:
    st.checkbox(task)

new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if selected_date in st.session_state.tasks:
        st.session_state.tasks[selected_date].append(new_task)
    else:
        st.session_state.tasks[selected_date] = [new_task]
    st.success(f"Task '{new_task}' added to {selected_date}!")
    # Pop-up style notification
    notification = st.empty()
    notification.info(f"🔔 New Task Added: '{new_task}' on {selected_date}")
    time.sleep(2)
    notification.empty()

# --------------------------
# Reminders Section
# --------------------------
st.subheader("⏰ Reminders")
reminder_date = st.date_input("Select reminder date", datetime.now())
reminder_msg = st.text_input("Enter reminder message", key="reminder_input")
if st.button("Add Reminder"):
    st.success(f"Reminder set for {reminder_date}: {reminder_msg}")
    # Pop-up style notification
    notification = st.empty()
    notification.info(f"🔔 Reminder: '{reminder_msg}' scheduled on {reminder_date}")
    time.sleep(2)
    notification.empty()

# --------------------------
# Chat Section (Dummy Responses)
# --------------------------
st.subheader("💬 Chat with AutoBot (Dummy Responses)")
user_input = st.text_input("Type your message", key="chat_input")
if st.button("Send Message"):
    response = random.choice(st.session_state.dummy_responses)
    st.markdown(f"**AutoBot:** {response}")

# --------------------------
# Payment Section
# --------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
st.write("Upcoming payments (dummy data):")
for p in st.session_state.payments:
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")
    # Pop-up notification if payment due today
    if datetime.now().date() == datetime.strptime(p['due'], "%Y-%m-%d").date():
        notification = st.empty()
        notification.warning(f"🔔 Payment Reminder: {p['name']} of {p['amount']} is due today!")
        time.sleep(2)
        notification.empty()

# --------------------------
# End of App
# --------------------------
st.write("---")
st.write("Made with ❤️ by Sabarni Guha")
