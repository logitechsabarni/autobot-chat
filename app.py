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

# Create all images in-memory
user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")
reminder_img = create_dummy_image((150, 255, 200), text="Rem")

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# --------------------------
# Sidebar: User Profile & Quick Links
# --------------------------
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
st.sidebar.button("View Reminders")
st.sidebar.markdown("---")

# --------------------------
# Initialize session state
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "2025-10-18": ["Pay electricity bill", "Team meeting 5 PM"],
        "2025-10-19": ["Doctor appointment", "Submit report"],
        "2025-10-20": ["Buy groceries", "Gym session"],
    }
if "reminders" not in st.session_state:
    st.session_state.reminders = [
        {"task": "Pay electricity bill", "datetime": "2025-10-18 10:00"},
        {"task": "Team meeting", "datetime": "2025-10-18 17:00"}
    ]
if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"},
    ]

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage your **tasks, calendar events, reminders, and payments** from a single hub!")

# --------------------------
# Task Overview Cards
# --------------------------
st.subheader("📊 Task Overview")
completed_tasks = sum(len(v) for k,v in st.session_state.tasks.items()[:1])
upcoming_tasks = sum(len(v) for k,v in st.session_state.tasks.items())
reminders_today = sum(1 for r in st.session_state.reminders if r["datetime"].startswith(datetime.now().strftime("%Y-%m-%d")))

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{completed_tasks} / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", f"{upcoming_tasks}", "-1 from yesterday")
col3.metric("Reminders Today", f"{reminders_today}", "+1 from yesterday")

# --------------------------
# Calendar Section
# --------------------------
st.subheader("📅 Calendar")
dates = list(st.session_state.tasks.keys())
selected_date = st.selectbox("Select a date", dates)
st.write(f"### Tasks for {selected_date}")
for task in st.session_state.tasks[selected_date]:
    st.checkbox(task)

new_task = st.text_input("Add a new task")
if st.button("Add Task"):
    if new_task.strip():
        st.session_state.tasks[selected_date].append(new_task)
        st.success(f"Task '{new_task}' added to {selected_date}!")

# --------------------------
# Reminders Section
# --------------------------
st.subheader("⏰ Reminders")
for rem in st.session_state.reminders:
    rem_time = datetime.strptime(rem["datetime"], "%Y-%m-%d %H:%M")
    st.write(f"- **{rem['task']}** at {rem_time.strftime('%b %d, %Y %I:%M %p')}")

new_reminder_task = st.text_input("New Reminder Task", key="rem_task")
new_reminder_date = st.date_input("Reminder Date", value=datetime.now(), key="rem_date")
new_reminder_time = st.time_input("Reminder Time", value=datetime.now().time(), key="rem_time")

if st.button("Add Reminder"):
    dt_str = datetime.combine(new_reminder_date, new_reminder_time).strftime("%Y-%m-%d %H:%M")
    st.session_state.reminders.append({"task": new_reminder_task, "datetime": dt_str})
    st.success(f"Reminder '{new_reminder_task}' scheduled for {dt_str}")

# Browser notification simulation
for rem in st.session_state.reminders:
    rem_time = datetime.strptime(rem["datetime"], "%Y-%m-%d %H:%M")
    now = datetime.now()
    if now >= rem_time and now <= rem_time + timedelta(minutes=1):
        st.markdown(f"""
        <script>
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {{
            var notification = new Notification("⏰ Reminder", {{
                body: "{rem['task']} is due now!",
                icon: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
            }});
        }}
        </script>
        """, unsafe_allow_html=True)

# --------------------------
# Payments Section
# --------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
st.write("Upcoming payments:")
for p in st.session_state.payments:
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")

# --------------------------
# Chat Section with Dummy Responses
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
    "Make sure to submit your reports before the deadline.",
    "Review your meetings for tomorrow.",
    "Check your emails for urgent tasks.",
    "Plan your breaks to maintain productivity.",
    "Remember to backup your files today.",
    "Prepare your weekly summary for the team meeting.",
    "Organize your workspace to stay efficient.",
    "Delegate tasks if overloaded.",
    "Update your progress tracker today.",
    "Set priorities for the most important tasks first."
]

user_input = st.text_input("Type your message here", key="chat_input")
if st.button("Send Message"):
    if user_input.strip():
        response = random.choice(dummy_responses)
        st.markdown(f"**AutoBot:** {response}")
