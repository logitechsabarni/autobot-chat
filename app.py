import streamlit as st
from PIL import Image, ImageDraw
from datetime import datetime, timedelta
import random
from streamlit_autorefresh import st_autorefresh

# -----------------------------
# Helper Functions
# -----------------------------
def create_dummy_image(color, size=(100, 100), text=None):
    img = Image.new("RGB", size, color)
    if text:
        draw = ImageDraw.Draw(img)
        draw.text((10, 40), text, fill="white")
    return img

def schedule_realistic_notification(title, message, notify_time):
    """Schedules a realistic browser notification with app-style styling"""
    now = datetime.now()
    delay = (notify_time - now).total_seconds() * 1000  # milliseconds
    if delay > 0:
        st.markdown(f"""
        <script>
        if (Notification.permission !== "granted") {{
            Notification.requestPermission();
        }} else {{
            setTimeout(function(){{
                var n = new Notification("{title}", {{
                    body: "{message}",
                    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
                    badge: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png"
                }});
                setTimeout(n.close.bind(n), 8000);
            }}, {int(delay)});
        }}
        </script>
        """, unsafe_allow_html=True)

def count_unread_notifications():
    unread = 0
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    for r in st.session_state.reminders:
        if r["datetime"] >= now_str and not r.get("read", False):
            unread += 1
    for p in st.session_state.payments:
        if datetime.strptime(p["due"], "%Y-%m-%d %H:%M") >= datetime.now() and not p.get("read", False):
            unread += 1
    return unread

def display_notifications():
    st.subheader("🔔 Notifications")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    notifications_shown = False
    for r in st.session_state.reminders:
        if r["datetime"] >= now_str and not r.get("read", False):
            st.info(f"Task Reminder: **{r['task']}** at {r['datetime']}")
            r["read"] = True
            notifications_shown = True
    for p in st.session_state.payments:
        due_dt = datetime.strptime(p['due'], "%Y-%m-%d %H:%M")
        if due_dt >= datetime.now() and not p.get("read", False):
            st.warning(f"Payment Reminder: **{p['name']}** | Amount: {p['amount']} | Due: {p['due']}")
            p["read"] = True
            notifications_shown = True
    if not notifications_shown:
        st.info("No new notifications.")

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
        {"name": "Electricity Bill", "amount": "$50", "due": "2025-10-18 10:00"},
        {"name": "Internet Bill", "amount": "$30", "due": "2025-10-20 12:00"},
        {"name": "Netflix Subscription", "amount": "$15", "due": "2025-10-19 09:00"},
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Live Refresh for Notifications (every 5 seconds)
# -----------------------------
st_autorefresh(interval=5000, key="notification_refresh")

# -----------------------------
# Top Notification Bell
# -----------------------------
unread_count = count_unread_notifications()
st.markdown(f"""
<div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 10px;">
    <button onclick="document.getElementById('notification_panel').style.display='block'" style="position: relative; padding: 10px 15px; font-size: 20px; cursor:pointer;">
        🔔
        <span style="position: absolute; top: -5px; right: -5px; background:red; color:white; border-radius:50%; padding:2px 6px; font-size:12px;">{unread_count}</span>
    </button>
</div>
<div id="notification_panel" style="display:none; border:1px solid #ddd; padding:10px; border-radius:10px; background:#f9f9f9;">
    <h4>Notifications</h4>
</div>
""", unsafe_allow_html=True)

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
upcoming_tasks = total_tasks
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
        reminder_datetime = datetime.combine(selected_date, reminder_time)
        st.session_state.reminders.append({"task": new_task, "datetime": reminder_datetime.strftime("%Y-%m-%d %H:%M"), "read": False})
        schedule_realistic_notification("Task Reminder", new_task, reminder_datetime)
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
    pay_datetime = datetime.strptime(p['due'], "%Y-%m-%d %H:%M")
    notify_datetime = pay_datetime - timedelta(hours=1)
    schedule_realistic_notification("Payment Reminder", f"{p['name']} is due at {p['due']}", notify_datetime)

# -----------------------------
# Dummy Chat Section
# -----------------------------
st.subheader("💬 Chat with AutoBot (Dummy Responses)")
dummy_responses = [
    "Don't forget your meeting at 5 PM today!", "You have 3 upcoming tasks this week.",
    "Reminder: Pay your electricity bill on time.", "Great job completing your tasks!",
    "Try to finish your pending reports today.", "Your next appointment is on 2025-10-19.",
    "Don't forget to review your emails.", "Keep up the productivity! 💪",
    "You have a new task to add: 'Prepare presentation'.", "Check your calendar for upcoming deadlines.",
    "Have you completed your weekly review?", "It's a good day to plan your tasks.",
    "Reminder: Team meeting tomorrow at 3 PM.", "Schedule your breaks to stay productive.",
    "Your tasks are on track for this week.", "Don't forget to update your progress.",
    "New task suggestion: 'Read AI research papers'.", "Stay focused and avoid distractions.",
    "Next reminder: 2025-10-20 09:00 AM", "You've completed 8 tasks this week. Awesome!",
    "Remember to send the report to the manager.", "Plan your tasks for tomorrow evening.",
    "Add 'Call client' to your to-do list.", "Don't forget to backup your files.",
    "Check your emails before the end of the day.", "Take a short break to stay fresh!",
    "Update your progress on the dashboard.", "Review last week's completed tasks.",
    "Prepare notes for the next meeting.", "Time to check pending payments.",
    "Great day to complete your remaining tasks!"
]

user_input = st.text_input("Type your message", key="chat_input")
if st.button("Send Message"):
    if user_input:
        response = random.choice(dummy_responses)
        st.session_state.chat_history.append({"user": user_input, "bot": response})
        st.markdown(f"**AutoBot:** {response}")

# -----------------------------
# Display Notification Panel if clicked
# -----------------------------
display_notifications()
