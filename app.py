import streamlit as st
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
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        (datetime.today()).strftime("%Y-%m-%d"): ["Sample task 1", "Sample task 2"]
    }
if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": (datetime.today()).strftime("%Y-%m-%d"), "paid": False},
        {"name": "Internet Bill", "amount": "$30", "due": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d"), "paid": False},
    ]
if "notifications" not in st.session_state:
    st.session_state.notifications = []

# --------------------------
# Sidebar: User Profile (Dynamic)
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")

today = datetime.today().date()
tasks_completed = sum(
    1 for date, tasks in st.session_state.tasks.items()
    if datetime.strptime(date, "%Y-%m-%d").date() < today
)
upcoming_tasks = sum(
    len(tasks) for date, tasks in st.session_state.tasks.items()
    if datetime.strptime(date, "%Y-%m-%d").date() >= today
)
reminders_today = len([n for n in st.session_state.notifications if "today" in n.lower()])

# Dynamic payment status
pending_payments = sum(1 for p in st.session_state.payments if not p["paid"])
st.sidebar.write(f"**Tasks Completed:** {tasks_completed}")
st.sidebar.write(f"**Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write(f"**Reminders Today:** {reminders_today}")
st.sidebar.write(f"**Pending Payments:** {pending_payments}")

# Next reminder (tasks or payments)
future_notifications = [n for n in st.session_state.notifications if "today" not in n.lower()]
next_reminder = future_notifications[0] if future_notifications else "No upcoming reminders"
st.sidebar.write(f"**Next Reminder:** {next_reminder}")
st.sidebar.markdown("---")

# --------------------------
# Sidebar: Quick Links
# --------------------------
st.sidebar.markdown("### 📌 Quick Links")
st.sidebar.button("View Calendar")
st.sidebar.button("View Tasks")
st.sidebar.button("Payments")
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

tasks_for_date = st.session_state.tasks.get(selected_date_str, [])
st.write(f"### Tasks for {selected_date_str}")
for idx, task in enumerate(tasks_for_date):
    checked = st.checkbox(task, key=f"{selected_date_str}_{idx}")
    if checked:
        st.session_state.notifications.append(f"Task '{task}' completed today!")

# Add new task
new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if selected_date_str in st.session_state.tasks:
        st.session_state.tasks[selected_date_str].append(new_task)
    else:
        st.session_state.tasks[selected_date_str] = [new_task]
    st.success(f"Task '{new_task}' added to {selected_date_str}!")

# --------------------------
# Payments Section (Dynamic)
# --------------------------
st.subheader("💰 Payments")
for idx, p in enumerate(st.session_state.payments):
    label = f"{p['name']} | Amount: {p['amount']} | Due: {p['due']}"
    paid_checkbox = st.checkbox(label, key=f"pay_{idx}", value=p["paid"])
    if paid_checkbox and not p["paid"]:
        p["paid"] = True
        st.session_state.notifications.append(f"Payment '{p['name']}' marked as PAID!")
    elif not paid_checkbox and p["paid"]:
        p["paid"] = False
        st.session_state.notifications.append(f"Payment '{p['name']}' marked as UNPAID!")

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
    "Don't forget your daily stand-up meeting.",
    "You have a new payment due: 'Gym Subscription'.",
    "Check your weekly goals progress.",
    "Time to update your task tracker.",
    "Schedule focus sessions for tomorrow."
]

user_input = st.text_input("Type your message")
if st.button("Send Message"):
    response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {response}")
    st.session_state.notifications.append(response)

# --------------------------
# Notifications Section
# --------------------------
st.subheader("🔔 Notifications")
if st.session_state.notifications:
    for note in st.session_state.notifications[-5:]:  # last 5 notifications
        st.info(note)
