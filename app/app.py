"""The main Streamlit app."""
import streamlit as st

import chart
import helper

st.title("Personal finances overview")

history_df = helper.load_data()
f"{len(history_df)} entries"
f"from {history_df['date'].min().date()} to {history_df['date'].max().date()}"

st.header("Absolute balance")
"Loans excluded"

balance_df = helper.get_daily_balance(history_df)

st.altair_chart(chart.create_balance_chart(balance_df), use_container_width=True)
