import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime, timedelta
import time

# --------------------------
# Helper functions
# --------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

def show_notification(message, kind="info", duration=2):
    """Show a temporary pop-up notification at top"""
    notification = st.empty()
    if kind == "info":
        notification.info(f"🔔 {message}")
    elif kind == "warning":
        notification.warning(f"⚠️ {message}")
    elif kind == "success":
        notification.success(f"✅ {message}")
    time.sleep(duration)
    notification.empty()

# --------------------------
# Dummy images
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
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18", "status": "Pending"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20", "status": "Pending"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19", "status": "Pending"},
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
# Sidebar
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
completed_tasks = sum([len(v) for v in st.session_state.tasks.values()]) - 5
upcoming_tasks = 5
st.sidebar.write(f"**Tasks Completed:** {completed_tasks} / 15")
st.sidebar.write(f"**Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write("**Next Reminder:** 2025-10-18 10:00 AM")
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
# Top Icons: Calendar, Payments
# --------------------------
st.subheader("🔹 Quick Access")
icon_col1, icon_col2 = st.columns(2)
with icon_col1:
    if st.button("📅 Calendar"):
        st.session_state.show_calendar = True
with icon_col2:
    if st.button("💰 Payments"):
        st.session_state.show_payments = True

# --------------------------
# Calendar Section
# --------------------------
if "show_calendar" not in st.session_state:
    st.session_state.show_calendar = False

if st.session_state.show_calendar:
    st.subheader("📅 Calendar & Tasks")
    selected_date = st.date_input("Select date", datetime.now())
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    tasks_for_date = st.session_state.tasks.get(selected_date_str, [])
    st.write(f"### Tasks for {selected_date_str}")
    for task in tasks_for_date:
        st.checkbox(task)
    new_task = st.text_input("Add new task", key=f"task_{selected_date_str}")
    if st.button("Add Task to Calendar"):
        st.session_state.tasks.setdefault(selected_date_str, []).append(new_task)
        show_notification(f"New task '{new_task}' added for {selected_date_str}", "success")

# --------------------------
# Payments Section
# --------------------------
if "show_payments" not in st.session_state:
    st.session_state.show_payments = False

if st.session_state.show_payments:
    st.subheader("💰 Payments")
    today = datetime.now().date()
    for p in st.session_state.payments:
        status = p["status"]
        due_date = datetime.strptime(p["due"], "%Y-%m-%d").date()
        st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']} | Status: {status}")
        if status == "Pending" and due_date <= today:
            show_notification(f"Payment '{p['name']}' of {p['amount']} is due!", "warning")
    # Add payment
    new_payment_name = st.text_input("Payment Name", key="payment_name")
    new_payment_amount = st.text_input("Amount", key="payment_amount")
    new_payment_due = st.date_input("Due Date", key="payment_due")
    if st.button("Add Payment"):
        st.session_state.payments.append({
            "name": new_payment_name,
            "amount": new_payment_amount,
            "due": new_payment_due.strftime("%Y-%m-%d"),
            "status": "Pending"
        })
        show_notification(f"Payment '{new_payment_name}' scheduled for {new_payment_due}", "success")

# --------------------------
# Reminders Section
# --------------------------
st.subheader("⏰ Reminders")
reminder_date = st.date_input("Select reminder date", datetime.now(), key="reminder_date")
reminder_msg = st.text_input("Enter reminder message", key="reminder_msg")
if st.button("Add Reminder"):
    show_notification(f"Reminder set: '{reminder_msg}' on {reminder_date}", "info")

# --------------------------
# Dummy Chat Section
# --------------------------
st.subheader("💬 Chat with AutoBot (Dummy Responses)")
user_input = st.text_input("Type your message", key="chat_input2")
if st.button("Send Message"):
    response = random.choice(st.session_state.dummy_responses)
    st.markdown(f"**AutoBot:** {response}")

# --------------------------
# Footer
# --------------------------
st.write("---")
st.write("Made with ❤️ by Sabarni Guha")
