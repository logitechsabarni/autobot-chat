import streamlit as st
from PIL import Image, ImageDraw
import random
from datetime import datetime, date, timedelta

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
# Browser Notification
# --------------------------
def send_browser_notification(message, title="AutoBot Reminder"):
    st.markdown(
        f"""
        <script>
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {{
            new Notification("{title}", {{ body: "{message}" }});
        }}
        </script>
        """,
        unsafe_allow_html=True,
    )

# --------------------------
# Create in-memory images
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
if "tasks_on_date" not in st.session_state:
    st.session_state.tasks_on_date = {}

if "payments" not in st.session_state:
    st.session_state.payments = []

# --------------------------
# Sidebar: User Profile
# --------------------------
st.sidebar.markdown("### 👤 User Profile")
st.sidebar.image(user_img, width=100)
st.sidebar.write("**Username:** Sabarni Guha")
total_tasks = sum(len(tasks) for tasks in st.session_state.tasks_on_date.values())
upcoming_tasks = sum(len(tasks) for d, tasks in st.session_state.tasks_on_date.items() if d >= date.today().strftime("%Y-%m-%d"))
st.sidebar.write("**Tasks Completed:** 8 / 15")
st.sidebar.write("**Upcoming Tasks:**", upcoming_tasks)
today_str = date.today().strftime("%Y-%m-%d")
reminders_today = st.session_state.tasks_on_date.get(today_str, [])
st.sidebar.write(f"**Reminders Today:** {len(reminders_today)}")
for r in reminders_today:
    st.sidebar.info(f"⏰ {r}")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Links")
st.sidebar.button("View Calendar")
st.sidebar.button("View Tasks")
st.sidebar.button("Payments")
st.sidebar.markdown("---")

# --------------------------
# Notifications for today
# --------------------------
for r in reminders_today:
    send_browser_notification(r, title="Task Reminder")

for p in st.session_state.payments:
    if not p["paid"] and p["due"] == today_str:
        send_browser_notification(f"{p['name']} of {p['amount']} is due today!", title="Payment Reminder")

# --------------------------
# Main Dashboard
# --------------------------
st.title("🤖 AutoBot Dashboard")
st.write("Manage **tasks, calendar events, payments, and reminders** from a single hub!")

# --------------------------
# Task Overview Cards
# --------------------------
st.subheader("📊 Task Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Tasks Completed", "8 / 15", "+2 from yesterday")
col2.metric("Upcoming Tasks", str(upcoming_tasks), "-1 from yesterday")
col3.metric("Reminders Today", str(len(reminders_today)), "+1 from yesterday")

# --------------------------
# Calendar & Task Scheduling
# --------------------------
st.subheader("📅 Calendar & Task Scheduling")
selected_date = st.date_input("Pick a date", date.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

# Display existing tasks
st.markdown(f"### Tasks for {selected_date_str}")
tasks = st.session_state.tasks_on_date.get(selected_date_str, [])
for t in tasks:
    st.checkbox(t, key=f"{selected_date_str}_{t}")

# Add new task
new_task = st.text_input(f"Add new task for {selected_date_str}")
if st.button(f"Add Task for {selected_date_str}"):
    if new_task.strip() != "":
        if selected_date_str in st.session_state.tasks_on_date:
            st.session_state.tasks_on_date[selected_date_str].append(new_task)
        else:
            st.session_state.tasks_on_date[selected_date_str] = [new_task]
        st.success(f"Task '{new_task}' added to {selected_date_str}!")
        send_browser_notification(f"New task added: {new_task}", title="Task Added")
    else:
        st.warning("Please enter a task before adding.")

# --------------------------
# Payments Section
# --------------------------
st.subheader("💰 Payments")
st.image(payment_img, width=80)
payment_name = st.text_input("Payment Name")
payment_amount = st.text_input("Amount ($)")
payment_due = st.date_input("Due Date", date.today())
if st.button("Add Payment"):
    if payment_name.strip() != "" and payment_amount.strip() != "":
        st.session_state.payments.append({"name": payment_name, "amount": f"${payment_amount}", "due": payment_due.strftime("%Y-%m-%d"), "paid": False})
        st.success(f"Payment '{payment_name}' added for {payment_due.strftime('%Y-%m-%d')}!")
        send_browser_notification(f"New payment added: {payment_name}", title="Payment Added")
    else:
        st.warning("Enter both payment name and amount.")

st.write("Existing Payments:")
for p in st.session_state.payments:
    status = "✅ Paid" if p["paid"] else "❌ Pending"
    st.write(f"- **{p['name']}** | Amount: {p['amount']} | Due: {p['due']} | Status: {status}")
    if not p["paid"] and st.button(f"Mark {p['name']} as Paid"):
        p["paid"] = True
        st.success(f"{p['name']} marked as paid!")
        send_browser_notification(f"{p['name']} marked as paid.", title="Payment Update")

# --------------------------
# Contextual Dummy Chat
# --------------------------
st.subheader("💬 Chat with AutoBot")
user_input = st.text_input("Type your message")
if st.button("Send Message") and user_input.strip() != "":
    # Dummy contextual responses
    responses = [
        "Keep up the productivity! 💪",
        "Great job completing your tasks!",
        "Don't forget to take breaks while working.",
        "Plan your week ahead to stay on track.",
        "Remember to check your calendar for upcoming events.",
        "Stay focused and avoid distractions.",
        "Remember to prioritize your tasks for today.",
        "It's a good day to review your progress.",
        "Check pending payments to avoid late fees.",
        "New tasks can be added to your calendar anytime.",
        "Review your reminders to stay on schedule.",
        "You're doing great! Keep going.",
        "Don't forget your meetings today.",
        "Your tasks are on track for the week.",
        "Stay consistent with your routine!",
        "Review your completed tasks for satisfaction.",
        "Remember to schedule breaks for better productivity.",
        "Pending payments might be due soon.",
        "Your calendar is filling up nicely.",
        "Try to finish important tasks first.",
        "Keep checking AutoBot for reminders.",
        "Update your task progress regularly.",
        "Check for overlapping meetings today.",
        "Good time to plan for tomorrow's tasks.",
        "Your workflow looks efficient!",
        "Reminder: Check your upcoming tasks today!",
        "Don't forget to mark completed payments.",
        "Plan your day with AutoBot for maximum efficiency.",
    ]
    
    response = random.choice(responses)
    st.markdown(f"**AutoBot:** {response}")
