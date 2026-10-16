from pathlib import Path
import duckdb
import pandas as pd

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "football_analytics.duckdb"
RAW_DIR = BASE_DIR / "Data" / "Raw"
DATA_DIR = BASE_DIR / "Data"

print("\n" + "=" * 60)
print("AFL MEMBER INTELLIGENCE — FINAL PROJECT VALIDATION")
print("=" * 60)

failures = []


def check(name, condition, actual=None, expected=None):
    if condition:
        print(f"✓ {name}")
    else:
        print(f"✗ {name}")
        failures.append(name)

        if expected is not None:
            print(f"  Expected: {expected}")
        if actual is not None:
            print(f"  Actual:   {actual}")


# ------------------------------------------------------------
# 1. REQUIRED FILES
# ------------------------------------------------------------
print("\n[1] REQUIRED FILES")

required_files = [
    DB_PATH,
    RAW_DIR / "afl_matches_2025.csv",
    RAW_DIR / "synthetic_members.csv",
    RAW_DIR / "synthetic_member_attendance.csv",
    RAW_DIR / "synthetic_transactions.csv",
    DATA_DIR / "member_360.csv",
    DATA_DIR / "attendance_analysis.csv",
    DATA_DIR / "transaction_analysis.csv",
    BASE_DIR / "Dashboard" / "app.py",
    BASE_DIR / "Dashboard" / "pages" / "Match_Fan_Behaviour.py",
    BASE_DIR / "requirements.txt",
]

for path in required_files:
    check(
        f"{path.relative_to(BASE_DIR)} exists",
        path.exists()
    )


# ------------------------------------------------------------
# 2. DATABASE CONNECTION
# ------------------------------------------------------------
print("\n[2] DATABASE")

try:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    print("✓ DuckDB connection successful")
except Exception as exc:
    print(f"✗ DuckDB connection failed: {exc}")
    raise


tables = con.execute("""
    SELECT table_name, table_type
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name
""").fetchdf()

print("\nDatabase objects:")
print(tables.to_string(index=False))


# ------------------------------------------------------------
# 3. MEMBERS
# ------------------------------------------------------------
print("\n[3] MEMBERS")

member_stats = con.execute("""
    SELECT
        COUNT(*) AS rows,
        COUNT(DISTINCT member_id) AS unique_members,
        SUM(CASE WHEN member_id IS NULL THEN 1 ELSE 0 END) AS null_ids
    FROM members
""").fetchone()

check("5,000 member rows", member_stats[0] == 5000,
      member_stats[0], 5000)

check("5,000 unique member IDs", member_stats[1] == 5000,
      member_stats[1], 5000)

check("No null member IDs", member_stats[2] == 0,
      member_stats[2], 0)


# ------------------------------------------------------------
# 4. MATCH DATA
# ------------------------------------------------------------
print("\n[4] AFL MATCH DATA")

match_stats = con.execute("""
    SELECT
        COUNT(*) AS matches,
        COUNT(DISTINCT match_id) AS unique_matches
    FROM matches
""").fetchone()

check("216 AFL matches", match_stats[0] == 216,
      match_stats[0], 216)

check("216 unique match IDs", match_stats[1] == 216,
      match_stats[1], 216)


richmond = con.execute("""
    SELECT
        COUNT(*) AS home_matches,
        ROUND(AVG(attendance), 0) AS avg_attendance,
        MAX(attendance) AS highest_attendance,
        SUM(
            CASE
                WHEN home_score > away_score THEN 1
                ELSE 0
            END
        ) AS home_wins
    FROM matches
    WHERE LOWER(TRIM(home_team)) = 'richmond'
""").fetchone()

check("12 Richmond home matches", richmond[0] == 12,
      richmond[0], 12)

check("Average Richmond home attendance = 41,534",
      int(richmond[1]) == 41534,
      richmond[1], 41534)

check("Highest Richmond home attendance = 80,009",
      richmond[2] == 80009,
      richmond[2], 80009)

check("Richmond home wins = 4",
      richmond[3] == 4,
      richmond[3], 4)


# ------------------------------------------------------------
# 5. ATTENDANCE FACT TABLE
# ------------------------------------------------------------
print("\n[5] MEMBER ATTENDANCE")

attendance_stats = con.execute("""
    SELECT
        COUNT(*) AS rows,
        COUNT(DISTINCT (member_id, match_id)) AS unique_events
    FROM member_attendance
""").fetchone()

check("23,759 attendance events",
      attendance_stats[0] == 23759,
      attendance_stats[0], 23759)

check("No duplicate member-match events",
      attendance_stats[0] == attendance_stats[1],
      attendance_stats[1], attendance_stats[0])


attendance_orphans = con.execute("""
    SELECT COUNT(*)
    FROM member_attendance a
    LEFT JOIN members m
        ON a.member_id = m.member_id
    LEFT JOIN matches mt
        ON a.match_id = mt.match_id
    WHERE m.member_id IS NULL
       OR mt.match_id IS NULL
""").fetchone()[0]

check("No attendance orphan records",
      attendance_orphans == 0,
      attendance_orphans, 0)


# ------------------------------------------------------------
# 6. TRANSACTIONS
# ------------------------------------------------------------
print("\n[6] TRANSACTIONS")

transaction_stats = con.execute("""
    SELECT
        COUNT(*) AS transactions,
        COUNT(DISTINCT member_id) AS purchasing_members,
        ROUND(SUM(amount), 2) AS revenue,
        ROUND(AVG(amount), 2) AS avg_transaction
    FROM transactions
""").fetchone()

check("8,726 transactions",
      transaction_stats[0] == 8726,
      transaction_stats[0], 8726)

check("4,040 purchasing members",
      transaction_stats[1] == 4040,
      transaction_stats[1], 4040)

check("Total simulated revenue = $643,955.56",
      abs(float(transaction_stats[2]) - 643955.56) < 0.01,
      transaction_stats[2], 643955.56)

check("Average transaction = $73.80",
      abs(float(transaction_stats[3]) - 73.80) < 0.01,
      transaction_stats[3], 73.80)


transaction_orphans = con.execute("""
    SELECT COUNT(*)
    FROM transactions t
    LEFT JOIN members m
        ON t.member_id = m.member_id
    WHERE m.member_id IS NULL
""").fetchone()[0]

check("No transaction orphan records",
      transaction_orphans == 0,
      transaction_orphans, 0)


# ------------------------------------------------------------
# 7. MEMBER 360
# ------------------------------------------------------------
print("\n[7] MEMBER 360 REPORTING VIEW")

m360 = con.execute("""
    SELECT
        COUNT(*) AS rows,
        COUNT(DISTINCT member_id) AS unique_members,
        ROUND(AVG(CAST(renewed_2026 AS INTEGER)) * 100, 1)
            AS renewal_rate,
        ROUND(AVG(total_spend), 2) AS avg_spend,
        ROUND(AVG(matches_attended), 1) AS avg_matches
    FROM member_360
""").fetchone()

check("member_360 contains 5,000 rows",
      m360[0] == 5000,
      m360[0], 5000)

check("member_360 contains 5,000 unique members",
      m360[1] == 5000,
      m360[1], 5000)

check("Renewal rate = 61.6%",
      float(m360[2]) == 61.6,
      m360[2], 61.6)

check("Average spend ≈ $128.79",
      abs(float(m360[3]) - 128.79) < 0.02,
      m360[3], 128.79)

check("Average matches attended = 4.8",
      float(m360[4]) == 4.8,
      m360[4], 4.8)


# ------------------------------------------------------------
# 8. MEMBER 360 DATA QUALITY
# ------------------------------------------------------------
print("\n[8] DATA QUALITY")

quality = con.execute("""
    SELECT
        SUM(CASE WHEN member_id IS NULL THEN 1 ELSE 0 END),
        SUM(CASE WHEN matches_attended < 0 THEN 1 ELSE 0 END),
        SUM(CASE WHEN total_spend < 0 THEN 1 ELSE 0 END),
        SUM(
            CASE
                WHEN email_open_rate < 0
                  OR email_open_rate > 1
                THEN 1 ELSE 0
            END
        )
    FROM member_360
""").fetchone()

check("No missing member IDs", quality[0] == 0,
      quality[0], 0)

check("No negative attendance", quality[1] == 0,
      quality[1], 0)

check("No negative spend", quality[2] == 0,
      quality[2], 0)

check("Email open rates within 0–1", quality[3] == 0,
      quality[3], 0)


# ------------------------------------------------------------
# 9. EXPORTED REPORTING DATA
# ------------------------------------------------------------
print("\n[9] REPORTING EXPORTS")

member_export = pd.read_csv(
    DATA_DIR / "member_360.csv"
)

attendance_export = pd.read_csv(
    DATA_DIR / "attendance_analysis.csv"
)

transaction_export = pd.read_csv(
    DATA_DIR / "transaction_analysis.csv"
)

check("member_360.csv has 5,000 rows",
      len(member_export) == 5000,
      len(member_export), 5000)

check("attendance_analysis.csv is not empty",
      len(attendance_export) > 0,
      len(attendance_export), "> 0")

check("transaction_analysis.csv is not empty",
      len(transaction_export) > 0,
      len(transaction_export), "> 0")


# ------------------------------------------------------------
# FINAL RESULT
# ------------------------------------------------------------
con.close()

print("\n" + "=" * 60)

if not failures:
    print("✓ ALL VALIDATION CHECKS PASSED")
    print("Project data is internally consistent.")
else:
    print(f"✗ {len(failures)} VALIDATION CHECK(S) FAILED")
    print("\nFailed checks:")
    for failure in failures:
        print(f" - {failure}")

print("=" * 60 + "\n")