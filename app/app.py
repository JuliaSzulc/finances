"""The main Streamlit app."""
import streamlit as st

import chart
import data

st.set_page_config(page_title="Personal finances overview", page_icon="📊")

st.title("Personal finances overview")

history_df = data.load_data()
f"{len(history_df)} entries"
f"from {history_df['date'].min().date()} to {history_df['date'].max().date()}"

st.header("Absolute balance")
"(loans excluded)"

balance_resolution = st.radio(
    "Resolution:", ("days", "months"), horizontal=True, label_visibility="collapsed"
)
balance_df = data.get_daily_balance(history_df)

if balance_resolution == "days":
    st.altair_chart(chart.create_balance_chart(balance_df), use_container_width=True)
else:
    st.altair_chart(
        chart.create_balance_chart(balance_df[balance_df["date"].dt.day == 1]),
        use_container_width=True,
    )

st.header("Incomes vs. expenses")
st.altair_chart(
    chart.create_expenses_incomes_chart(data.get_monthly_incomes_expenses(history_df))
)


st.header("Monthly average per category")
n_months = st.slider(
    "Based on last n months:", 1, len(history_df["date"].dt.to_period("M").unique()), 12
)
st.dataframe(
    data.get_mean_categories(history_df, n_months=n_months),
    width=400,
    height=570,
)
