import streamlit as st
from PIL import Image, ImageDraw
from datetime import datetime, timedelta
import random

# -----------------------------
# Helper functions
# -----------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

def schedule_browser_notification(task_name, task_datetime):
    """Schedules a browser notification for a given task"""
    now = datetime.now()
    delay = (task_datetime - now).total_seconds() * 1000  # milliseconds
    if delay > 0:
        st.markdown(f"""
        <script>
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {{
            setTimeout(function(){{
                new Notification("⏰ Reminder", {{
                    body: "{task_name} is due now!",
                    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
                }});
            }}, {int(delay)});
        }}
        </script>
        """, unsafe_allow_html=True)

# -----------------------------
# Dummy images
# -----------------------------
user_img = create_dummy_image((255, 200, 150), text="User")
task_img = create_dummy_image((100, 200, 255), text="Task")
calendar_img = create_dummy_image((200, 255, 100), text="Cal")
payment_img = create_dummy_image((255, 150, 150), text="Pay")

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="💬", layout="wide")

# -----------------------------
# Initialize Session State
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = {}
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19"},
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Sidebar: Profile & Links
# -----------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
st.sidebar.write(f"**Tasks Completed:** {sum([len(v) for v in st.session_state.tasks.values()])} / 15")
st.sidebar.write(f"**Upcoming Tasks:** {sum([len(v) for v in st.session_state.tasks.values()])}")
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
st.write("Manage your **tasks, calendar events, payments, and reminders** from one place!")

# -----------------------------
# Task Overview Cards
# -----------------------------
st.subheader("📊 Task Overview")
total_tasks = sum([len(v) for v in st.session_state.tasks.values()])
upcoming_tasks = total_tasks  # Dummy
reminders_today = sum([1 for r in st.session_state.reminders if r['datetime'].startswith(datetime.today().strftime("%Y-%m-%d"))])

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", f"{total_tasks} / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", f"{upcoming_tasks}", "-1 from yesterday")
col3.metric("Reminders Today", f"{reminders_today}", "+1 from yesterday")

# -----------------------------
# Calendar & Task Scheduler
# -----------------------------
st.subheader("📅 Calendar & Task Scheduler")
selected_date = st.date_input("Select a date", datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

st.write(f"### Tasks for {selected_date_str}")
tasks_for_date = st.session_state.tasks.get(selected_date_str, [])
for i, task in enumerate(tasks_for_date):
    st.checkbox(task, key=f"{selected_date_str}_{i}")

new_task = st.text_input("Add a new task", key="new_task")
reminder_time = st.time_input("Set Reminder Time", value=datetime.now().time(), key="reminder_time")

if st.button("Add Task"):
    if new_task:
        if selected_date_str in st.session_state.tasks:
            st.session_state.tasks[selected_date_str].append(new_task)
        else:
            st.session_state.tasks[selected_date_str] = [new_task]
        # Add reminder
        reminder_datetime = datetime.combine(selected_date, reminder_time)
        st.session_state.reminders.append({"task": new_task, "datetime": reminder_datetime.strftime("%Y-%m-%d %H:%M")})
        schedule_browser_notification(new_task, reminder_datetime)
        st.success(f"Task '{new_task}' scheduled on {selected_date_str} at {reminder_time}!")

# -----------------------------
# Reminders Section
# -----------------------------
st.subheader("⏰ Upcoming Reminders")
if st.session_state.reminders:
    for r in st.session_state.reminders:
        st.write(f"- **{r['task']}** at {r['datetime']}")
else:
    st.info("No reminders scheduled yet.")

# -----------------------------
# Payments Section
# -----------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
st.write("Upcoming payments:")
for p in st.session_state.payments:
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")

# -----------------------------
# Dummy Chat Section
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
    "You've completed 8 tasks this week. Awesome!",
    "Remember to send the report to the manager.",
    "Plan your tasks for tomorrow evening.",
    "Add 'Call client' to your to-do list.",
    "Don't forget to backup your files.",
    "Check your emails before the end of the day.",
    "Take a short break to stay fresh!",
    "Update your progress on the dashboard.",
    "Review last week's completed tasks.",
    "Prepare notes for the next meeting.",
    "Time to check pending payments.",
    "Great day to complete your remaining tasks!"
]

user_input = st.text_input("Type your message", key="chat_input")
if st.button("Send Message"):
    if user_input:
        response = random.choice(dummy_responses)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        st.markdown(f"**AutoBot:** {response}")
