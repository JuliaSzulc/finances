"""Altair charts definitions"""
import altair as alt
import pandas as pd


def create_balance_chart(balance_df: pd.DataFrame) -> alt.Chart:
    """
    Creates an interactive chart of absolute balance in time.

    Args:
        balance_df: Balance DataFrame including `date` and `balance` columns.

    Returns:
        Altair chart.
    """
    line = (
        alt.Chart(balance_df)
        .mark_line()
        .encode(
            alt.X("date:T", title=None, axis=alt.Axis(format="%b %y", labelAngle=-70)),
            alt.Y("balance:Q", title="balance [SEK]"),
        )
    )

    selection_nearest = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    tooltips = (
        alt.Chart(balance_df)
        .mark_rule(color="white")
        .encode(
            x="date:T",
            opacity=alt.condition(selection_nearest, alt.value(0.5), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", format="%d %b %Y"),
                alt.Tooltip("balance:Q", format=",.2f"),
            ],
        )
        .add_selection(selection_nearest)
    )

    points = line.mark_point().encode(
        opacity=alt.condition(selection_nearest, alt.value(1), alt.value(0))
    )

    return (line + tooltips + points).interactive()


def create_expenses_incomes_chart(expenses_incomes_df: pd.DataFrame) -> alt.Chart:
    """
    Creates a bar chart of monthly aggregated incomes and expenses.

    Args:
        expenses_incomes_df: DataFrame including `date`, `type` and `amount` columns.

    Returns:
        Altair chart.
    """
    bars = (
        alt.Chart(expenses_incomes_df)
        .mark_bar()
        .encode(
            x=alt.X("type:N", title="", sort="descending"),
            y=alt.Y("amount:Q", title="amount [SEK]"),
            color=alt.Color(
                "type:N",
                sort="descending",
                scale=alt.Scale(range=["mediumseagreen", "indianred"]),
            ),
            column="yearmonth(date):T",
        )
        .configure_legend(
            orient="top",
            title=None,
        )
        .configure_header(title=None)
        .configure_facet(spacing=5)
    )

    return bars
