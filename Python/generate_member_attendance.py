import duckdb
import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

np.random.seed(42)

DATABASE_PATH = "football_analytics.duckdb"


# --------------------------------------------------
# 2. Connect to DuckDB
# --------------------------------------------------

connection = duckdb.connect(DATABASE_PATH)


# --------------------------------------------------
# 3. Load members
# --------------------------------------------------

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


# --------------------------------------------------
# 4. Load Richmond home matches
# --------------------------------------------------

richmond_matches = connection.sql("""
    SELECT
        match_id,
        date,
        home_team,
        away_team,
        venue
    FROM matches
    WHERE home_team = 'Richmond'
""").df()


print("Members loaded:", len(members))
print("Richmond home matches:", len(richmond_matches))


# --------------------------------------------------
# 5. Generate member attendance
# --------------------------------------------------

attendance_records = []

for _, member in members.iterrows():

    # Calculate email open rate safely
    if member["emails_sent"] > 0:
        email_open_rate = (
            member["emails_opened"]
            / member["emails_sent"]
        )
    else:
        email_open_rate = 0

    # Start with a base probability of attending a home match
    attendance_probability = 0.20

    # Higher membership tiers are somewhat more likely to attend
    if member["membership_tier"] == "Silver":
        attendance_probability += 0.08

    elif member["membership_tier"] == "Gold":
        attendance_probability += 0.18

    elif member["membership_tier"] == "Premium":
        attendance_probability += 0.28

    # Longer-term members are slightly more likely to attend
    attendance_probability += min(
        member["years_as_member"] * 0.008,
        0.12
    )

    # Digitally engaged members are somewhat more likely to attend
    attendance_probability += email_open_rate * 0.10

    attendance_probability += min(
        member["app_sessions"] * 0.003,
        0.08
    )

    # Prevent unrealistic probabilities
    attendance_probability = np.clip(
        attendance_probability,
        0.10,
        0.85
    )

    # Decide attendance separately for each Richmond home match
    for _, match in richmond_matches.iterrows():

        attended = (
            np.random.random()
            < attendance_probability
        )

        if attended:
            attendance_records.append({
                "member_id": int(member["member_id"]),
                "match_id": int(match["match_id"])
            })


# --------------------------------------------------
# 6. Create attendance DataFrame
# --------------------------------------------------

member_attendance = pd.DataFrame(
    attendance_records
)


# --------------------------------------------------
# 7. Validate
# --------------------------------------------------

print("\nATTENDANCE CHECKS:")

print(
    "Attendance records:",
    len(member_attendance)
)

print(
    "Members who attended at least one match:",
    member_attendance["member_id"].nunique()
)

print(
    "Matches represented:",
    member_attendance["match_id"].nunique()
)

average_matches = (
    len(member_attendance)
    / len(members)
)

print(
    "Average matches attended per member:",
    round(average_matches, 2)
)


# --------------------------------------------------
# 8. Save dataset
# --------------------------------------------------

output_path = "Data/Raw/synthetic_member_attendance.csv"

member_attendance.to_csv(
    output_path,
    index=False
)

print(
    "\nSynthetic attendance dataset saved to:",
    output_path
)


# --------------------------------------------------
# 9. Close database connection
# --------------------------------------------------

connection.close()