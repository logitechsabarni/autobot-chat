import streamlit as st
from datetime import datetime, timedelta
import random

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="AutoBot Dashboard", page_icon="🤖", layout="wide")

# ------------------------------
# Initialize Session State
# ------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        (datetime.today()).strftime("%Y-%m-%d"): ["Finish project report", "Team meeting 5 PM"],
        (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d"): ["Client follow-up", "Submit assignment"]
    }

if "payments" not in st.session_state:
    st.session_state.payments = [
        {"name": "Electricity Bill", "amount": "₹800", "due": (datetime.today()).strftime("%Y-%m-%d"), "paid": False},
        {"name": "Netflix Subscription", "amount": "₹499", "due": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d"), "paid": False},
        {"name": "Internet Bill", "amount": "₹699", "due": (datetime.today() + timedelta(days=5)).strftime("%Y-%m-%d"), "paid": True},
    ]

if "notifications" not in st.session_state:
    st.session_state.notifications = []

# ------------------------------
# Sidebar: Profile + Summary
# ------------------------------
st.sidebar.title("👤 User Panel")
st.sidebar.markdown("**Name:** Sabarni Guha")
st.sidebar.markdown("**Role:** User")
st.sidebar.markdown("---")

today = datetime.today().date()
tasks_completed = sum(
    1 for date, task_list in st.session_state.tasks.items()
    if datetime.strptime(date, "%Y-%m-%d").date() < today
)
upcoming_tasks = sum(
    len(task_list) for date, task_list in st.session_state.tasks.items()
    if datetime.strptime(date, "%Y-%m-%d").date() >= today
)
pending_payments = sum(1 for p in st.session_state.payments if not p["paid"])

st.sidebar.write(f"✅ **Tasks Completed:** {tasks_completed}")
st.sidebar.write(f"🕒 **Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write(f"💰 **Pending Payments:** {pending_payments}")
st.sidebar.markdown("---")

# ------------------------------
# Dashboard Header
# ------------------------------
st.title("🤖 AutoBot Interactive Dashboard")
st.write("Welcome to your AI-powered productivity dashboard — manage your **tasks, reminders, and payments** seamlessly!")

# ------------------------------
# Calendar & Task Section
# ------------------------------
st.subheader("📅 Calendar and Task Manager")

selected_date = st.date_input("Select a date to view tasks", datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

tasks = st.session_state.tasks.get(selected_date_str, [])
if tasks:
    for i, task in enumerate(tasks):
        checked = st.checkbox(task, key=f"task_{selected_date_str}_{i}")
        if checked:
            st.session_state.notifications.append(f"✅ Task '{task}' completed on {selected_date_str}")
else:
    st.info("No tasks scheduled for this date.")

new_task = st.text_input("Add a new task")
if st.button("➕ Add Task"):
    if selected_date_str in st.session_state.tasks:
        st.session_state.tasks[selected_date_str].append(new_task)
    else:
        st.session_state.tasks[selected_date_str] = [new_task]
    st.success(f"Task '{new_task}' added to {selected_date_str}!")
    st.session_state.notifications.append(f"🗓️ New Task Added: {new_task} on {selected_date_str}")

# ------------------------------
# Payments Section
# ------------------------------
st.subheader("💳 Payments and Dues")

for idx, payment in enumerate(st.session_state.payments):
    label = f"{payment['name']} — {payment['amount']} — Due: {payment['due']}"
    paid = st.checkbox(label, value=payment["paid"], key=f"pay_{idx}")

    if paid and not payment["paid"]:
        payment["paid"] = True
        st.session_state.notifications.append(f"✅ Payment completed: {payment['name']}")
    elif not paid and payment["paid"]:
        payment["paid"] = False
        st.session_state.notifications.append(f"⚠️ Payment marked as pending: {payment['name']}")

with st.expander("➕ Add a new payment"):
    pay_name = st.text_input("Payment Name")
    pay_amount = st.text_input("Amount (e.g., ₹500)")
    pay_due = st.date_input("Due Date", datetime.today() + timedelta(days=3))
    if st.button("Add Payment"):
        st.session_state.payments.append({
            "name": pay_name,
            "amount": pay_amount,
            "due": pay_due.strftime("%Y-%m-%d"),
            "paid": False
        })
        st.success(f"Payment '{pay_name}' added successfully!")
        st.session_state.notifications.append(f"💰 New Payment Added: {pay_name} due on {pay_due.strftime('%Y-%m-%d')}")

# ------------------------------
# Hackathon Chat Section (Dynamic Claude-style responses with context)
# ------------------------------
st.subheader("💬 Chat with AutoBot")

# Keyword-based responses referencing actual tasks/payments
claude_responses_map = {
    "schedule": [
        f"Meeting scheduled! Your tasks for {selected_date_str}: {tasks}" if tasks else "Meeting scheduled! Your calendar is free.",
        "Your new meeting is on the calendar 📅",
        "Scheduled successfully! Don’t forget to check your agenda 🗓️"
    ],
    "remind": [
        f"Reminder set! Pending payments: {[p['name'] for p in st.session_state.payments if not p['paid']]}",
        "Got it! I will remind you at the scheduled time ⏰",
        "Reminder confirmed! You won't forget this task ✅"
    ],
    "payment": [
        f"Payment info: {[p['name']+' ('+p['amount']+')' for p in st.session_state.payments]}",
        "Payment scheduled successfully 💳",
        "Payment recorded in your dashboard ✅"
    ],
    "task": [
        f"Task list updated for {selected_date_str}: {tasks}" if tasks else "No tasks yet, but new task added ✅",
        "New task added to your list 📝",
        "Task logged successfully! Stay productive 💪"
    ],
    "default": [
        "Got it! Task recorded. ✅",
        "Understood! Logged successfully 🗒️",
        "Noted! I’ll keep track of this 📝",
        "Okay! Added to your dashboard 📌",
        "Copy that! Everything is on track ✅",
        "Message received! You’re all set 🌟",
        "Sure! I’ve noted it down 🗒️",
        "Done! Your instructions are saved ✅",
        "Acknowledged! Your dashboard is updated 📅",
        "All set! Keep going 💪",
        "Noted! Don’t forget to check your tasks 🕒",
        "All caught! You’re on track 🌟",
        "Recorded! AutoBot has got your back 🤖",
        "Logged successfully! Keep it up ✅",
        "Understood! Reminder added ⏰",
        "Noted! Task and reminders updated 📝",
        "Great! Your schedule looks updated 📅",
        "Confirmed! All actions recorded ✅",
        "Message noted! Continue with your day 💡",
        "Acknowledged! Dashboard updated 🗒️"
    ]
}

user_msg = st.text_input("Type your message here")
if st.button("Send"):
    if user_msg.strip() != "":
        user_lower = user_msg.lower()
        bot_response = random.choice(claude_responses_map["default"])  # default response

        # Match keyword and pick realistic response
        for key, resp_list in claude_responses_map.items():
            if key in user_lower:
                bot_response = random.choice(resp_list)
                break

        st.markdown(f"**AutoBot:** {bot_response}")
        st.session_state.notifications.append(f"💬 AutoBot says: {bot_response}")
    else:
        st.warning("Please type a message first!")

# ------------------------------
# Notifications Section
# ------------------------------
st.subheader("🔔 Notifications")
if st.session_state.notifications:
    for note in st.session_state.notifications[-6:]:  # show latest 6
        st.info(note)
else:
    st.write("No notifications yet.")
