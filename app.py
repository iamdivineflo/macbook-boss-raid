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
    .metric-card {
        background-color: #1a1c23;
        border: 1px solid #ff7518;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "macbook_cost" not in st.session_state:
    st.session_state.macbook_cost = 1500.0
if "current_saved" not in st.session_state:
    st.session_state.current_saved = 0.0
if "boss_hp" not in st.session_state:
    st.session_state.boss_hp = 1500.0
if "history" not in st.session_state:
    st.session_state.history = []

st.title("👻 MacBook Boss Raid: Ghost Edition")
st.write(
    "Exorcise the matrix, crush the ghost's regeneration, and lock in your studio hardware."
)

# Sidebar: Campaign Setup
st.sidebar.header("Campaign Settings")
target_goal = st.sidebar.number_input(
    "MacBook Target Cost ($)", value=st.session_state.macbook_cost, step=100.0
)
if target_goal != st.session_state.macbook_cost:
    st.session_state.macbook_cost = target_goal
    st.session_state.boss_hp = max(0.0, target_goal - st.session_state.current_saved)

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
    with st.form("damage_form"):
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
            st.session_state.history.append(
                {
                    "Type": "Damage (Income)",
                    "Platform/Source": platform,
                    "Amount": dash_amount,
                    "Details": f"Instant Payout via {platform}",
                }
            )
            st.success(
                f"Critical Hit! Dealt ${dash_amount:.2f} damage to the ghost via {platform}."
            )

# Action 2: Boss Regeneration (Expenses / Gas)
with col2:
    st.markdown("### 🩸 Specter Regen (Expenses)")
    with st.form("regen_form"):
        expense_amount = st.number_input(
            "Expense Amount ($)", min_value=0.0, step=1.0
        )
        expense_desc = st.text_input(
            "Description (e.g., Gas, Equipment)", value="Gas"
        )
        expense_submit = st.form_submit_button("🔮 Log Overhead")
        if expense_submit and expense_amount > 0:
            st.session_state.boss_hp += expense_amount
            st.session_state.history.append(
                {
                    "Type": "Regeneration (Expense)",
                    "Platform/Source": "Overhead",
                    "Amount": expense_amount,
                    "Details": expense_desc,
                }
            )
            st.warning(
                f"The ghost regenerated ${expense_amount:.2f} via {expense_desc}!"
            )

# Combat Ledger & Excel/CSV Export
st.markdown("---")
st.subheader("📜 Sovereign Ledger")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    df.index = df.index + 1  # 1-based indexing for clean tracking
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
