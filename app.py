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

if "user_name" not in st.session_state:
    st.session_state.user_name = "Sabarni Guha"

# ------------------------------
# Helper: Update Stats
# ------------------------------
def update_stats():
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
    return tasks_completed, upcoming_tasks, pending_payments

# ------------------------------
# Sidebar: Profile + Summary
# ------------------------------
st.sidebar.title("👤 User Panel")
st.sidebar.markdown(f"**Name:** {st.session_state.user_name}")
st.sidebar.markdown("**Role:** User")
st.sidebar.markdown("---")

tasks_completed, upcoming_tasks, pending_payments = update_stats()

st.sidebar.write(f"✅ **Tasks Completed:** {tasks_completed}")
st.sidebar.write(f"🕒 **Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write(f"💰 **Pending Payments:** {pending_payments}")
st.sidebar.markdown("---")

# ------------------------------
# Dashboard Header
# ------------------------------
st.title(f"🤖 Hi {st.session_state.user_name}! Welcome to AutoBot Dashboard")
st.write("Manage your **tasks, reminders, and payments** efficiently with AI-style assistance!")

# ------------------------------
# Calendar & Task Section
# ------------------------------
st.subheader("📅 Calendar and Task Manager")

selected_date = st.date_input("Select a date to view tasks", datetime.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

tasks = st.session_state.tasks.get(selected_date_str, [])
if tasks:
    for i, task in enumerate(tasks.copy()):
        checked = st.checkbox(task, value=False, key=f"task_{selected_date_str}_{i}")
        if checked:
            st.session_state.notifications.append(f"✅ Task '{task}' completed on {selected_date_str}")
            # Mark it completed by removing from upcoming tasks
            tasks.remove(task)
            st.session_state.tasks[selected_date_str] = tasks
else:
    st.info("No tasks scheduled for this date.")

# Add a new task
new_task = st.text_input("Add a new task")
if st.button("➕ Add Task"):
    if new_task.strip() != "":
        if selected_date_str in st.session_state.tasks:
            st.session_state.tasks[selected_date_str].append(new_task)
        else:
            st.session_state.tasks[selected_date_str] = [new_task]
        st.success(f"Task '{new_task}' added to {selected_date_str}!")
        st.session_state.notifications.append(f"🗓️ New Task Added: {new_task} on {selected_date_str}")
    else:
        st.warning("Please type a task!")

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

# Add new payment
with st.expander("➕ Add a new payment"):
    pay_name = st.text_input("Payment Name")
    pay_amount = st.text_input("Amount (e.g., ₹500)")
    pay_due = st.date_input("Due Date", datetime.today() + timedelta(days=3))
    if st.button("Add Payment Now"):
        if pay_name.strip() != "" and pay_amount.strip() != "":
            st.session_state.payments.append({
                "name": pay_name,
                "amount": pay_amount,
                "due": pay_due.strftime("%Y-%m-%d"),
                "paid": False
            })
            st.success(f"Payment '{pay_name}' added successfully!")
            st.session_state.notifications.append(f"💰 New Payment Added: {pay_name} due on {pay_due.strftime('%Y-%m-%d')}")
        else:
            st.warning("Please fill both name and amount!")

# ------------------------------
# Chat Section (Offline Claude-style)
# ------------------------------
st.subheader("💬 Chat with AutoBot")

claude_responses_map = {
    "greeting": [
        "Hii! How can I help you today?",
        f"Hello {st.session_state.user_name}! What would you like to do?",
        "Hey there! Ready to manage your tasks and payments?"
    ],
    "schedule": [
        f"Meeting scheduled. Your tasks for {selected_date_str}: {tasks}" if tasks else "Meeting scheduled! Your calendar is free today.",
        "Meeting confirmed 📅",
        "Scheduled successfully! Check your agenda 🗓️"
    ],
    "remind": [
        f"Reminder set. Pending payments: {[p['name'] for p in st.session_state.payments if not p['paid']]}",
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
        "Got it! ✅",
        "Understood! Logged successfully 🗒️",
        "Noted! I’ll keep track of this 📝",
        "Okay! Added to your dashboard 📌",
        "Message received! You’re all set 🌟",
        "Done! Your instructions are saved ✅"
    ]
}

user_msg = st.text_input("Type your message here")
if st.button("Send"):
    if user_msg.strip() != "":
        user_lower = user_msg.lower()
        bot_response = random.choice(claude_responses_map["default"])

        # Greeting check first
        if any(greet in user_lower for greet in ["hi", "hello", "hey", "hii"]):
            bot_response = random.choice(claude_responses_map["greeting"])
        else:
            for key, resp_list in claude_responses_map.items():
                if key != "greeting" and key in user_lower:
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
    for note in st.session_state.notifications[-6:]:
        st.info(note)
else:
    st.write("No notifications yet.")

# ------------------------------
# Update Stats dynamically
# ------------------------------
tasks_completed, upcoming_tasks, pending_payments = update_stats()
st.sidebar.write(f"✅ **Tasks Completed:** {tasks_completed}")
st.sidebar.write(f"🕒 **Upcoming Tasks:** {upcoming_tasks}")
st.sidebar.write(f"💰 **Pending Payments:** {pending_payments}")
