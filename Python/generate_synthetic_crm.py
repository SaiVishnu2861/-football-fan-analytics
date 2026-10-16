import pandas as pd
import numpy as np


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

# Makes our synthetic data reproducible.
# Every time we run this script, we get the same dataset.
np.random.seed(42)

NUM_MEMBERS = 5000
CURRENT_YEAR = 2026


# --------------------------------------------------
# 2. Member identifiers and demographics
# --------------------------------------------------

# Create 5,000 unique fictional member IDs:
# 10001, 10002, 10003 ... 15000
member_ids = np.arange(
    10001,
    10001 + NUM_MEMBERS
)


# Generate ages using a normal (bell-shaped) distribution.
# Most members will be around age 40, with fewer very young/old members.
ages = np.random.normal(
    loc=40,
    scale=15,
    size=NUM_MEMBERS
)

# Prevent unrealistic ages and convert decimals to whole numbers.
ages = np.clip(
    ages,
    16,
    85
).astype(int)


# Generate broad geographic regions.
# These probabilities are fictional and exist only for the simulation.
regions = np.random.choice(
    [
        "Inner Melbourne",
        "Eastern Suburbs",
        "Northern Suburbs",
        "Western Suburbs",
        "South-Eastern Suburbs",
        "Regional Victoria"
    ],
    size=NUM_MEMBERS,
    p=[
        0.18,
        0.22,
        0.16,
        0.12,
        0.20,
        0.12
    ]
)


# --------------------------------------------------
# 3. Membership characteristics
# --------------------------------------------------

# Generate fictional membership tiers.
membership_tiers = np.random.choice(
    [
        "Bronze",
        "Silver",
        "Gold",
        "Premium"
    ],
    size=NUM_MEMBERS,
    p=[
        0.40,
        0.30,
        0.20,
        0.10
    ]
)


# Generate membership tenure.
# Exponential distribution means many newer members
# and progressively fewer very long-term members.
raw_tenure = np.random.exponential(
    scale=5,
    size=NUM_MEMBERS
)

years_as_member = np.clip(
    raw_tenure,
    0,
    25
).astype(int)


# Derive join year from tenure.
# We derive it instead of generating it separately so the
# two columns can never contradict each other.
join_year = CURRENT_YEAR - years_as_member


# --------------------------------------------------
# 4. Auto-renew behaviour
# --------------------------------------------------

# Everyone starts with a base probability of using auto-renew.
#
# We then make auto-renew somewhat more likely for:
# - longer-tenure members
# - Gold members
# - Premium members
#
# These relationships are synthetic business assumptions,
# NOT real Richmond Football Club statistics.

auto_renew_probability = (
    0.35
    + 0.012 * years_as_member
    + np.where(
        membership_tiers == "Gold",
        0.08,
        0
    )
    + np.where(
        membership_tiers == "Premium",
        0.14,
        0
    )
)


# Keep every probability between 20% and 85%.
auto_renew_probability = np.clip(
    auto_renew_probability,
    0.20,
    0.85
)


# Generate True/False auto-renew status.
auto_renew = (
    np.random.random(NUM_MEMBERS)
    < auto_renew_probability
)


# --------------------------------------------------
# 5. Digital engagement behaviour
# --------------------------------------------------

# Number of marketing emails sent to each member.
emails_sent = np.random.randint(
    18,
    41,
    size=NUM_MEMBERS
)


# Give every fictional member an underlying engagement tendency.
#
# This is a hidden variable used to generate realistic relationships
# between email opens, clicks and app activity.
#
# It will NOT appear in the final CRM table.
engagement_tendency = np.random.beta(
    2.5,
    3.0,
    size=NUM_MEMBERS
)


# More engaged members are more likely to open emails.
email_open_rate = (
    0.12
    + 0.65 * engagement_tendency
)

email_open_rate = np.clip(
    email_open_rate,
    0.05,
    0.90
)


# Generate how many emails each member actually opened.
emails_opened = np.random.binomial(
    emails_sent,
    email_open_rate
)


# More engaged members are also more likely to click
# after opening an email.
click_probability = (
    0.05
    + 0.35 * engagement_tendency
)

click_probability = np.clip(
    click_probability,
    0.02,
    0.55
)


# Generate clicks.
#
# A member cannot click more emails than they opened because
# the number of trials here is emails_opened.
email_clicks = np.array([
    np.random.binomial(
        opened,
        probability
    )
    for opened, probability
    in zip(
        emails_opened,
        click_probability
    )
])


# Generate app usage.
# More engaged members generally have more app sessions.
app_sessions = np.random.poisson(
    lam=2 + 18 * engagement_tendency
)


# --------------------------------------------------
# 6. Membership renewal
# --------------------------------------------------

# Now we create our main business outcome:
#
# Did the member renew for 2026?
#
# Renewal is deliberately NOT completely random.
#
# It is influenced by:
# - years as a member
# - whether auto-renew is enabled
# - digital engagement
# - membership tier
#
# This gives us meaningful relationships to investigate later
# using SQL and our dashboard.

renewal_probability = (
    0.38
    + 0.012 * years_as_member
    + 0.20 * auto_renew.astype(int)
    + 0.16 * engagement_tendency
    + np.where(
        membership_tiers == "Gold",
        0.04,
        0
    )
    + np.where(
        membership_tiers == "Premium",
        0.07,
        0
    )
)


# Prevent probabilities going below 20% or above 95%.
renewal_probability = np.clip(
    renewal_probability,
    0.20,
    0.95
)


# Convert the probability into an actual True/False outcome.
renewed_2026 = (
    np.random.random(NUM_MEMBERS)
    < renewal_probability
)


# --------------------------------------------------
# 7. Build the member CRM table
# --------------------------------------------------

members = pd.DataFrame({
    "member_id": member_ids,
    "age": ages,
    "region": regions,
    "membership_tier": membership_tiers,
    "years_as_member": years_as_member,
    "join_year": join_year,
    "auto_renew": auto_renew,
    "emails_sent": emails_sent,
    "emails_opened": emails_opened,
    "email_clicks": email_clicks,
    "app_sessions": app_sessions,
    "renewed_2026": renewed_2026
})


# --------------------------------------------------
# 8. Validate the synthetic dataset
# --------------------------------------------------

print("\nFIRST 10 MEMBERS:")
print(members.head(10))


print("\nDATASET CHECKS:")

print(
    "Number of members:",
    len(members)
)

print(
    "Unique member IDs:",
    members["member_id"].nunique()
)

print(
    "Missing values:",
    members.isna().sum().sum()
)

print(
    "Average age:",
    round(
        members["age"].mean(),
        1
    )
)

print(
    "Renewal rate:",
    round(
        members["renewed_2026"].mean() * 100,
        1
    ),
    "%"
)

print(
    "Auto-renew rate:",
    round(
        members["auto_renew"].mean() * 100,
        1
    ),
    "%"
)


print("\nMEMBERSHIP TIER DISTRIBUTION:")

print(
    members["membership_tier"]
    .value_counts(normalize=True)
    .round(3)
)


# --------------------------------------------------
# 9. Save the synthetic CRM dataset
# --------------------------------------------------

output_path = "Data/Raw/synthetic_members.csv"

members.to_csv(
    output_path,
    index=False
)

print(
    "\nSynthetic member dataset saved to:",
    output_path
)