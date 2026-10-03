import json
import os
import pandas as pd
import streamlit as st

# Page Configuration & Spooky Dark Theme Styling
st.set_page_config(
    page_title="MacBook Boss Raid: Ghost Edition", layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

DATA_FILE = "boss_save_data.json"


# Load saved data from disk if it exists
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "macbook_cost": 8000.0,
        "current_saved": 0.0,
        "boss_hp": 8000.0,
        "history": [],
    }


# Save data to disk
def save_data():
    data = {
        "macbook_cost": st.session_state.macbook_cost,
        "current_saved": st.session_state.current_saved,
        "boss_hp": st.session_state.boss_hp,
        "history": st.session_state.history,
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# Initialize session state from file
saved_data = load_data()
if "macbook_cost" not in st.session_state:
    st.session_state.macbook_cost = saved_data["macbook_cost"]
if "current_saved" not in st.session_state:
    st.session_state.current_saved = saved_data["current_saved"]
if "boss_hp" not in st.session_state:
    st.session_state.boss_hp = saved_data["boss_hp"]
if "history" not in st.session_state:
    st.session_state.history = saved_data["history"]

st.title("👻 MacBook Boss Raid: Ghost Edition")
st.write(
    "Exorcise the matrix, crush the ghost's regeneration, and lock in your studio hardware."
)

# Sidebar: Campaign Setup
st.sidebar.header("Campaign Settings")
target_goal = st.sidebar.number_input(
    "MacBook Target Cost ($)",
    value=float(st.session_state.macbook_cost),
    step=100.0,
)
if target_goal != st.session_state.macbook_cost:
    st.session_state.macbook_cost = target_goal
    # Recalculate boss HP based on new goal minus what's saved
    st.session_state.boss_hp = max(
        0.0, target_goal - st.session_state.current_saved
    )
    save_data()

# Boss Health Status
st.subheader("👻 Haunting Specter Status (Boss HP)")
hp_percentage = max(
    0.0,
    min(
        1.0,
        (st.session_state.boss_hp / st.session_state.macbook_cost)
        if st.session_state.macbook_cost > 0
        else 0,
    ),
)
st.progress(hp_percentage)
st.metric(
    label="Specter HP (Remaining Goal)",
    value=f"${st.session_state.boss_hp:.2f}",
    delta=f"-${st.session_state.current_saved:.2f} Total Banished/Saved",
)

col1, col2 = st.columns(2)

# Action 1: Deal Damage (Multi-App Income)
with col1:
    st.markdown("### 🗡️ Deal Damage (Income)")
    with st.form("damage_form", clear_on_submit=True):
        platform = st.selectbox(
            "Select Gig Platform", ["DoorDash", "Walmart Spark", "Uber Eats"]
        )
        dash_amount = st.number_input("Shift Payout ($)", min_value=0.0, step=1.0)
        dash_submit = st.form_submit_button("👻 Strike Specter")
        if dash_submit and dash_amount > 0:
            st.session_state.current_saved += dash_amount
            st.session_state.boss_hp = max(
                0.0, st.session_state.boss_hp - dash_amount
            )
            st.session_state.history.insert(
                0,
                {
                    "Type": "Damage (Income)",
                    "Platform/Source": platform,
                    "Amount": dash_amount,
                    "Details": f"Instant Payout via {platform}",
                },
            )
            save_data()
            st.success(
                f"Critical Hit! Dealt ${dash_amount:.2f} damage to the ghost via {platform}."
            )
            st.rerun()

# Action 2: Boss Regeneration (Expenses / Gas)
with col2:
    st.markdown("### 🩸 Specter Regen (Expenses)")
    with st.form("regen_form", clear_on_submit=True):
        expense_amount = st.number_input(
            "Expense Amount ($)", min_value=0.0, step=1.0
        )
        expense_desc = st.text_input(
            "Description (e.g., Gas, Equipment)", value="Gas"
        )
        expense_submit = st.form_submit_button("🔮 Log Overhead")
        if expense_submit and expense_amount > 0:
            st.session_state.boss_hp += expense_amount
            st.session_state.history.insert(
                0,
                {
                    "Type": "Regeneration (Expense)",
                    "Platform/Source": "Overhead",
                    "Amount": expense_amount,
                    "Details": expense_desc,
                },
            )
            save_data()
            st.warning(
                f"The ghost regenerated ${expense_amount:.2f} via {expense_desc}!"
            )
            st.rerun()

# Combat Ledger & Excel/CSV Export
st.markdown("---")
st.subheader("📜 Sovereign Ledger")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    df.index = range(len(df), 0, -1)  # Clean row numbering
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Ledger (CSV/Excel)",
        data=csv,
        file_name="sovereign_budget_ledger.csv",
        mime="text/csv",
    )
else:
    st.info("No strikes logged yet. Run a shift, log your flow, and attack.")
