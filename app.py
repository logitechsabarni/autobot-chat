import streamlit as st
from datetime import datetime, timedelta
import random
from PIL import Image, ImageDraw

# -----------------------------
# Helper: Create dummy images
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
# Initialize session state
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = {}

if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"},
    ]

if "notifications" not in st.session_state:
    st.session_state.notifications = []

# -----------------------------
# Dummy chatbot responses
# -----------------------------
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
    "Remember to submit your report before 5 PM.",
    "You have pending payments to check.",
    "Don't forget to call your client.",
    "Schedule a workout session today.",
    "Review your project milestones for the week."
]

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="🤖 AutoBot Dashboard", page_icon="💬", layout="wide")

# -----------------------------
# Sidebar: User Profile & Quick Links
# -----------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
st.sidebar.write("**Tasks Completed:** 8 / 15")
st.sidebar.write("**Upcoming Tasks:** 5")
st.sidebar.write(f"**Next Reminder:** {datetime.today().strftime('%Y-%m-%d %I:%M %p')}")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📌 Quick Links")
st.sidebar.button("View Calendar")
st.sidebar.button("View Tasks")
st.sidebar.button("Payments")
st.sidebar.markdown("---")

# -----------------------------
# Main Dashboard
# -----------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, payments, and reminders** from a single hub!")

# -----------------------------
# Task Overview Cards
# -----------------------------
st.subheader("📊 Task Overview")
tasks_completed = sum(len(tasks) for tasks in st.session_state.tasks.values())
upcoming_tasks_count = sum(1 for date, tasks in st.session_state.tasks.items() 
                           if datetime.strptime(date, "%Y-%m-%d").date() >= datetime.today().date())
reminders_today = len([n for n in st.session_state.notifications 
                       if "scheduled for today" in n])

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{tasks_completed} / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", upcoming_tasks_count, "-1 from yesterday")
col3.metric("Reminders Today", reminders_today, "+1 from yesterday")

# -----------------------------
# Task Scheduler with Calendar
# -----------------------------
st.subheader("📅 Schedule Tasks")
task_name = st.text_input("Task Name", key="new_task_input")
task_date = st.date_input("Select Date", key="new_task_date")

if st.button("Add Task"):
    date_str = task_date.strftime("%Y-%m-%d")
    if date_str not in st.session_state.tasks:
        st.session_state.tasks[date_str] = []
    st.session_state.tasks[date_str].append(task_name)

    # Add notification for today
    if task_date == datetime.today().date():
        st.session_state.notifications.append(f"Reminder: '{task_name}' scheduled for today!")

    st.success(f"Task '{task_name}' scheduled for {date_str}!")

# Display upcoming tasks
st.subheader("📋 Upcoming Tasks")
today = datetime.today().date()
upcoming_tasks_list = []

for date_str, tasks in st.session_state.tasks.items():
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    for t in tasks:
        upcoming_tasks_list.append((date_obj, t))

upcoming_tasks_list.sort(key=lambda x: x[0])

for i, (d, t) in enumerate(upcoming_tasks_list):
    checked = st.checkbox(f"{d} - {t}", key=f"task_{i}")
    if checked and d == today:
        st.session_state.notifications.append(f"Task '{t}' completed today!")

# -----------------------------
# Payments Section
# -----------------------------
st.subheader("💰 Payments")
payment_name = st.text_input("Payment Name", key="new_payment_name")
payment_amount = st.text_input("Amount ($)", key="new_payment_amount")
payment_due = st.date_input("Due Date", key="new_payment_date")

if st.button("Add Payment"):
    st.session_state.payments.append({
        "name": payment_name,
        "amount": f"${payment_amount}",
        "due": payment_due.strftime("%Y-%m-%d")
    })
    if payment_due == today:
        st.session_state.notifications.append(f"Payment '{payment_name}' is due today!")
    st.success(f"Payment '{payment_name}' added for {payment_due.strftime('%Y-%m-%d')}!")

st.write("Upcoming Payments:")
for p in st.session_state.payments:
    due_date = datetime.strptime(p['due'], "%Y-%m-%d").date()
    status = "✅ Paid" if due_date < today else "⏰ Pending"
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']} | Status: {status}")

# -----------------------------
# Notifications Section
# -----------------------------
st.subheader("🔔 Notifications")
if st.session_state.notifications:
    for n in st.session_state.notifications:
        st.info(n)
else:
    st.info("No notifications at the moment!")

# -----------------------------
# Dummy Chatbot
# -----------------------------
st.subheader("💬 Chat with AutoBot")
user_input_chat = st.text_input("Ask AutoBot something...", key="chat_input")
if st.button("Send Message", key="chat_button"):
    response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {response}")
