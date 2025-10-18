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
# Notification helper
# --------------------------
def show_notification(message, type="info"):
    st.toast(message, icon="✅" if type=="success" else "⚠️")

# --------------------------
# Initialize session state
# --------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "2025-10-18": ["Pay electricity bill", "Team meeting 5 PM"],
        "2025-10-19": ["Doctor appointment", "Submit report"],
        "2025-10-20": ["Buy groceries", "Gym session"]
    }

if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"}
    ]

# --------------------------
# Create images
# --------------------------
user_img = create_dummy_image((255, 200, 150), text="User")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# --------------------------
# Sidebar: User Profile & Links
# --------------------------
with st.sidebar:
    st.markdown("### 👤 User Profile")
    st.image(user_img, width=100)
    st.write("**Username:** Sabarni Guha")
    st.write(f"**Tasks Completed:** {len(st.session_state.tasks)}")
    st.write(f"**Upcoming Tasks:** {sum(len(v) for k,v in st.session_state.tasks.items() if datetime.strptime(k, '%Y-%m-%d').date() >= datetime.now().date())}")
    st.markdown("---")
    st.markdown("### 📌 Quick Links")
    st.button("View Calendar")
    st.button("View Tasks")
    st.button("Payments")
    st.markdown("---")

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, payments, and reminders** from one hub!")

# --------------------------
# Helper: Calculate task stats dynamically
# --------------------------
def calculate_task_stats():
    today = datetime.now().date()
    completed = 0
    upcoming = 0
    reminders_today = 0
    for date_str, task_list in st.session_state.tasks.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if date_obj < today:
            completed += len(task_list)
        elif date_obj == today:
            reminders_today += len(task_list)
        else:
            upcoming += len(task_list)
    return completed, upcoming, reminders_today

completed_tasks, upcoming_tasks, reminders_today = calculate_task_stats()

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{completed_tasks}")
col2.metric("Upcoming Tasks", f"{upcoming_tasks}")
col3.metric("Reminders Today", f"{reminders_today}")

# --------------------------
# Calendar & Task Scheduling
# --------------------------
st.subheader("📅 Calendar")
dates = sorted(st.session_state.tasks.keys())
selected_date = st.selectbox("Select a date", dates)
st.write(f"### Tasks for {selected_date}")
for idx, task in enumerate(st.session_state.tasks[selected_date]):
    checked = st.checkbox(task, key=f"{selected_date}_{idx}")
    if checked:
        show_notification(f"✅ Task '{task}' completed!", "success")
        st.session_state.tasks[selected_date].pop(idx)
        st.experimental_rerun()

new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if selected_date in st.session_state.tasks:
        st.session_state.tasks[selected_date].append(new_task)
    else:
        st.session_state.tasks[selected_date] = [new_task]
    show_notification(f"📌 New task '{new_task}' added for {selected_date}", "success")
    st.experimental_rerun()

# --------------------------
# Payment Section
# --------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
st.write("Upcoming payments:")
for idx, p in enumerate(st.session_state.payments):
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")
    if datetime.strptime(p['due'], "%Y-%m-%d").date() <= datetime.now().date():
        show_notification(f"⚠️ Payment due today: {p['name']}", "info")

new_payment_name = st.text_input("Payment Name")
new_payment_amount = st.text_input("Amount")
new_payment_due = st.date_input("Due Date")
if st.button("Add Payment"):
    st.session_state.payments.append({
        "name": new_payment_name,
        "amount": f"${new_payment_amount}",
        "due": new_payment_due.strftime("%Y-%m-%d")
    })
    show_notification(f"💰 Payment '{new_payment_name}' scheduled for {new_payment_due}", "success")
    st.experimental_rerun()

# --------------------------
# Dummy Chatbot Section
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
    "Time to check your payments!",
    "Prepare your daily to-do list.",
    "Remember to drink water regularly.",
    "Weekly review is pending!",
    "Team collaboration session is tomorrow.",
    "Update your task priorities for today."
]

user_input = st.text_input("Type your message")
if st.button("Send Message"):
    response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {response}")
