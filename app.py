import streamlit as st
from streamlit import session_state as state
from PIL import Image, ImageDraw
import random
from datetime import datetime, timedelta

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
# Initialize images
# --------------------------
user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# --------------------------
# Initialize session state
# --------------------------
if "tasks" not in state:
    state.tasks = {
        (datetime.today()).strftime("%Y-%m-%d"): ["Sample task 1", "Sample task 2"]
    }
if "payments" not in state:
    state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": (datetime.today()).strftime("%Y-%m-%d")},
        {"name": "Internet Bill", "amount": "$30", "due": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")},
    ]
if "notifications" not in state:
    state.notifications = []

# --------------------------
# Sidebar: User Profile
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
st.sidebar.markdown("---")

# --------------------------
# Sidebar: Quick Links
# --------------------------
st.sidebar.markdown("### 📌 Quick Links")
if st.sidebar.button("View Calendar"):
    st.info("Select a date below to schedule tasks.")
if st.sidebar.button("View Tasks"):
    st.info("Check tasks for selected date below.")
if st.sidebar.button("Payments"):
    st.info("Check upcoming payments below.")
st.sidebar.markdown("---")

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, reminders, and payments** from a single hub!")

# --------------------------
# Calendar & Task Scheduler
# --------------------------
st.subheader("📅 Schedule / View Tasks")
selected_date = st.date_input("Select a date", datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

# Show tasks for the selected date
tasks_for_date = state.tasks.get(selected_date_str, [])
st.write(f"### Tasks for {selected_date_str}")
for idx, task in enumerate(tasks_for_date):
    checked = st.checkbox(task, key=f"{selected_date_str}_{idx}")
    if checked:
        state.notifications.append(f"Task '{task}' completed today!")

# Add new task
new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if selected_date_str in state.tasks:
        state.tasks[selected_date_str].append(new_task)
    else:
        state.tasks[selected_date_str] = [new_task]
    st.success(f"Task '{new_task}' added to {selected_date_str}!")

# --------------------------
# Payments Section
# --------------------------
st.subheader("💰 Payments")
for idx, p in enumerate(state.payments):
    paid = st.checkbox(f"{p['name']} | Amount: {p['amount']} | Due: {p['due']}", key=f"pay_{idx}")
    if paid:
        state.notifications.append(f"Payment '{p['name']}' marked as paid!")

# --------------------------
# Task Overview Cards (Dynamic)
# --------------------------
st.subheader("📊 Task Overview")
today = datetime.today().date()
tasks_completed = sum(1 for date, tasks in state.tasks.items() 
                      if datetime.strptime(date, "%Y-%m-%d").date() < today)
upcoming_tasks_count = sum(len(tasks) for date, tasks in state.tasks.items()
                           if datetime.strptime(date, "%Y-%m-%d").date() >= today)
reminders_today = len([n for n in state.notifications if "today" in n.lower()])

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{tasks_completed}")
col2.metric("Upcoming Tasks", upcoming_tasks_count)
col3.metric("Reminders Today", reminders_today)

# --------------------------
# Dummy Chat Section
# --------------------------
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
    "You've completed 8 tasks this week. Awesome!",
    "Remember to check your emails today.",
    "Meeting notes should be updated.",
    "Upcoming payment is due soon.",
    "Review your project deadlines.",
    "Plan tasks for tomorrow evening.",
    "Don't forget your daily stand-up meeting."
]

user_input = st.text_input("Type your message")
if st.button("Send Message"):
    response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {response}")
    state.notifications.append(response)

# --------------------------
# Notifications Section
# --------------------------
st.subheader("🔔 Notifications")
if state.notifications:
    for note in state.notifications[-5:]:  # show last 5 notifications
        st.info(note)
