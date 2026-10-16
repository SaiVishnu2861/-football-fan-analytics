import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# --------------------------------------------------
# 1. Download the AFL 2025 season webpage
# --------------------------------------------------

url = "https://afltables.com/afl/seas/2025.html"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# --------------------------------------------------
# 2. Find individual match tables
# --------------------------------------------------

tables = soup.find_all("table")

match_tables = []

for table in tables:
    text = table.get_text(" ", strip=True)

    if "Att:" in text and "Venue:" in text and table.find("table") is None:
        match_tables.append(table)


# --------------------------------------------------
# 3. Extract information from each match
# --------------------------------------------------

matches = []

for match in match_tables:

    rows = match.find_all("tr")

    if len(rows) != 2:
        continue

    home_cells = rows[0].find_all(["td", "th"])
    away_cells = rows[1].find_all(["td", "th"])

    if len(home_cells) < 4 or len(away_cells) < 3:
        continue

    home_team = home_cells[0].get_text(" ", strip=True)
    home_score = home_cells[2].get_text(" ", strip=True)

    away_team = away_cells[0].get_text(" ", strip=True)
    away_score = away_cells[2].get_text(" ", strip=True)

    match_info = home_cells[3].get_text(" ", strip=True)

    # Attendance
    attendance_match = re.search(r"Att:\s*([\d,]+)", match_info)

    if attendance_match:
        attendance = int(attendance_match.group(1).replace(",", ""))
    else:
        attendance = None

    # Venue
    venue_match = re.search(r"Venue:\s*(.+)$", match_info)

    if venue_match:
        venue = venue_match.group(1).strip()
    else:
        venue = None

    # Date and time
    datetime_match = re.search(
        r"\w{3}\s+(\d{2}-\w{3}-\d{4})\s+(\d{1,2}:\d{2}\s+[AP]M)",
        match_info
    )

    if datetime_match:
        match_date = datetime_match.group(1)
        match_time = datetime_match.group(2)
    else:
        match_date = None
        match_time = None

    # Store one structured match record
    matches.append({
        "date": match_date,
        "time": match_time,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": int(home_score),
        "away_score": int(away_score),
        "attendance": attendance,
        "venue": venue
    })


# --------------------------------------------------
# 4. Convert records into a DataFrame
# --------------------------------------------------

df = pd.DataFrame(matches)

print(df.head())
print("\nNumber of matches extracted:", len(df))
print("\nMissing values:")
print(df.isna().sum())

output_path = "Data/Raw/afl_matches_2025.csv"

df.to_csv(output_path, index=False)

print("\nDataset saved to:", output_path)