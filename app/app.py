"""The main Streamlit app."""
import streamlit as st

import chart
import helper

st.title("Personal finances overview")

history_df = helper.load_data()
f"{len(history_df)} entries"
f"from {history_df['date'].min().date()} to {history_df['date'].max().date()}"

st.header("Absolute balance")
"(loans excluded)"

balance_resolution = st.radio(
    "Resolution:", ("days", "months"), horizontal=True, label_visibility="collapsed"
)
balance_df = helper.get_daily_balance(history_df)

if balance_resolution == "days":
    st.altair_chart(chart.create_balance_chart(balance_df), use_container_width=True)
else:
    st.altair_chart(
        chart.create_balance_chart(balance_df[balance_df["date"].dt.day == 1]),
        use_container_width=True,
    )
