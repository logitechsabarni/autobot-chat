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

# Compute stats
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

# Sidebar Info
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

# Add a new task
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

# Add new payment
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
# Dummy Chat Section
# ------------------------------
st.subheader("💬 Chat with AutoBot")

dummy_responses = [
    "Your payment for Netflix is due soon!",
    "Great work completing your tasks today!",
    "You have 2 upcoming deadlines tomorrow.",
    "Remember to pay your electricity bill on time.",
    "Your tasks are on track — keep it up!",
    "Don’t forget to schedule your next project review.",
    "Payment reminder: Internet bill due this week.",
    "Task completed successfully! 🎉",
    "AutoBot: Stay productive and focused!",
    "Your calendar looks clear for the weekend.",
    "💡 Pro Tip: Try finishing your toughest task first.",
]

user_msg = st.text_input("Type your message here")
if st.button("Send"):
    bot_response = random.choice(dummy_responses)
    st.markdown(f"**AutoBot:** {bot_response}")
    st.session_state.notifications.append(f"💬 AutoBot says: {bot_response}")

# ------------------------------
# Notifications Section
# ------------------------------
st.subheader("🔔 Notifications")
if st.session_state.notifications:
    for note in st.session_state.notifications[-6:]:  # show latest 6
        st.info(note)
else:
    st.write("No notifications yet.")

