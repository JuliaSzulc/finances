"""Helper functions."""
import pandas as pd

with open("data/starting_balance.txt") as fp:
    _STARTING_BALANCE = float(fp.readline())


def load_data() -> pd.DataFrame:
    """
    Loads the whole history from `data/history.csv`.

    Returns:
        Formatted DataFrame ready to use.
    """
    df = pd.read_csv(
        "data/history.csv",
        parse_dates=["date"],
        dtype={
            "ref": "string",
            "info": "string",
            "amount": "float64",
            "category": "string",
            "balance": "float64",
        },
    )

    # just make sure that dates are ordered - they are but better to be safe
    assert pd.DatetimeIndex(df["date"]).is_monotonic_increasing, "Dates not ordered!"

    return df


def get_daily_balance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieves balance per day information and add missing dates for all present months.

    Note: Loans are excluded from balance calculation.

    Args:
        df: Chronological operation history DataFrame.

    Returns:
        Dataframe with date and balance columns.
    """
    # filter out loans
    balance_df = df[df["category"] != "loans"][["date", "amount"]]
    balance_df = balance_df.groupby("date").sum()

    # calculate balance
    balance_before = _STARTING_BALANCE
    for idx, row in balance_df.iterrows():
        balance = round(balance_before + row["amount"], 2)
        balance_df.loc[idx, "balance"] = balance
        balance_before = balance

    balance_df = balance_df.drop(columns=["amount"])

    # add missing days
    balance_df = balance_df.reindex(
        pd.date_range(
            balance_df.index[0].to_period("M").to_timestamp(),
            balance_df.index[-1],
        ),
        method="ffill",
        fill_value=balance_df["balance"][0],
    )
    balance_df = balance_df.reset_index(names="date")

    return balance_df


def get_monthly_incomes_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Groups by month and sums incomes and expenses.

    Args:
        df: Chronological operation history DataFrame.

    Returns:
        DataFrame with columns `date`, `type` ("income"/"expense") and `amount`.
    """
    incomes_expenses_df = (
        df.groupby([pd.Grouper(key="date", freq="M"), df["amount"] > 0])["amount"]
        .sum()
        .abs()
        .to_frame()
        .rename(index={False: "expenses", True: "incomes"})
        .reset_index(names=["date", "type"])
    )

    return incomes_expenses_df
