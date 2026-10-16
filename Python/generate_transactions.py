import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

np.random.seed(42)

DATABASE_PATH = "football_analytics.duckdb"


# --------------------------------------------------
# 2. Load member data
# --------------------------------------------------

connection = duckdb.connect(DATABASE_PATH)

members = connection.sql("""
    SELECT
        member_id,
        membership_tier,
        years_as_member,
        emails_sent,
        emails_opened,
        app_sessions
    FROM members
""").df()

print("Members loaded:", len(members))


# --------------------------------------------------
# 3. Generate transactions
# --------------------------------------------------

transactions = []

transaction_id = 1

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)

days_in_year = (end_date - start_date).days


for _, member in members.iterrows():

    # Calculate digital engagement
    email_open_rate = (
        member["emails_opened"] / member["emails_sent"]
        if member["emails_sent"] > 0
        else 0
    )

    # Base expected number of purchases
    purchase_rate = 0.8

    # Higher-tier members tend to purchase somewhat more
    if member["membership_tier"] == "Silver":
        purchase_rate += 0.3

    elif member["membership_tier"] == "Gold":
        purchase_rate += 0.7

    elif member["membership_tier"] == "Premium":
        purchase_rate += 1.1

    # Engagement also influences purchasing
    purchase_rate += email_open_rate * 0.8
    purchase_rate += min(member["app_sessions"] * 0.025, 0.5)

    # Generate number of transactions for this member
    number_of_transactions = np.random.poisson(
        lam=purchase_rate
    )

    for _ in range(number_of_transactions):

        # Generate transaction category
        category = np.random.choice(
            [
                "Merchandise",
                "Food & Beverage",
                "Event",
                "Ticket Upgrade"
            ],
            p=[
                0.45,
                0.25,
                0.15,
                0.15
            ]
        )

        # Different categories have different typical spend
        if category == "Merchandise":
            amount = np.random.normal(85, 30)

        elif category == "Food & Beverage":
            amount = np.random.normal(35, 12)

        elif category == "Event":
            amount = np.random.normal(120, 40)

        else:
            amount = np.random.normal(65, 20)

        # Prevent negative or tiny transaction values
        amount = max(amount, 5)

        # Generate random transaction date during 2025
        random_days = np.random.randint(
            0,
            days_in_year + 1
        )

        transaction_date = (
            start_date
            + timedelta(days=int(random_days))
        )

        transactions.append({
            "transaction_id": transaction_id,
            "member_id": int(member["member_id"]),
            "transaction_date": transaction_date.date(),
            "category": category,
            "amount": round(amount, 2)
        })

        transaction_id += 1


# --------------------------------------------------
# 4. Build transaction table
# --------------------------------------------------

transactions_df = pd.DataFrame(transactions)


# --------------------------------------------------
# 5. Validate
# --------------------------------------------------

print("\nTRANSACTION CHECKS:")

print(
    "Total transactions:",
    len(transactions_df)
)

print(
    "Members with transactions:",
    transactions_df["member_id"].nunique()
)

print(
    "Total simulated revenue: $",
    round(transactions_df["amount"].sum(), 2)
)

print(
    "Average transaction value: $",
    round(transactions_df["amount"].mean(), 2)
)

print("\nTransaction categories:")

print(
    transactions_df["category"].value_counts()
)


# --------------------------------------------------
# 6. Save
# --------------------------------------------------

output_path = "Data/Raw/synthetic_transactions.csv"

transactions_df.to_csv(
    output_path,
    index=False
)

print(
    "\nSynthetic transaction dataset saved to:",
    output_path
)

connection.close()