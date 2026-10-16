# AFL Member & Fan Intelligence

An end-to-end analytics portfolio project exploring **fan engagement, member retention, commercial performance and match-day behaviour** in an AFL context.

The project combines publicly available 2025 AFL match data with a simulated 5,000-member CRM dataset to demonstrate a complete analytics workflow — from data collection and relational modelling through SQL analysis, validation and interactive dashboards.

> **Independent portfolio project.** Public match data is sourced from AFL Tables. Member, transaction and member-attendance data is simulated. No proprietary Richmond Football Club data is used.

---

## Project Objective

The project was designed around a hypothetical analytics problem:

> **How could a football club combine membership, engagement, transaction and match data to better understand member retention, commercial value and match-day behaviour?**

The analysis focuses on four areas:

- Member retention and engagement
- Membership-tier performance
- Commercial and transaction behaviour
- Match attendance and fan behaviour

The project was developed as a portfolio case study relevant to customer, membership, marketing and commercial analytics roles.

---

## Analytics Pipeline

```text
Public AFL Match Data
        │
        ├──────────────┐
        │              │
Synthetic CRM      Synthetic Transactions
        │              │
        └──────┬───────┘
               │
     Synthetic Member Attendance
               │
               ▼
            DuckDB
               │
      Relational Data Model
               │
        SQL Analysis Layer
               │
      Data Quality Validation
               │
        Reporting Views
               │
               ▼
      Streamlit Dashboards
```

The workflow includes data extraction, synthetic data generation, relational joins, aggregation, data-quality testing, reporting-layer construction and interactive visualisation.

---

## Data

### Public AFL Match Data

2025 AFL match information was collected from **AFL Tables**, including:

- Match date
- Home and away teams
- Scores
- Stadium attendance
- Venue

The dataset contains **216 matches**, including **12 Richmond home matches** used in the match and fan-behaviour dashboard.

### Simulated CRM Data

A reproducible synthetic CRM population of **5,000 fictional members** was generated for the case study.

Features include:

- Age
- Region
- Membership tier
- Membership tenure
- Auto-renew status
- Email engagement
- App engagement
- 2026 renewal outcome

Synthetic relationships were deliberately introduced to create a realistic analytical environment. They must therefore be interpreted as **illustrative associations rather than findings about real Richmond members**.

### Simulated Member Attendance

Member-match attendance records represent one fictional member attending one Richmond home match.

The dataset contains:

- **23,759 member-match attendance events**
- 5,000 possible members
- 12 Richmond home fixtures

### Simulated Transactions

The commercial dataset contains:

- **8,726 transactions**
- **4,040 purchasing members**
- **$643,955.56 simulated revenue**
- Merchandise, events, ticket upgrades and food & beverage categories

---

## Data Model

The analytical model connects member, match, attendance and transaction data.

```text
members
   │
   │ member_id
   │
   ├──────────────< transactions
   │
   └──────────────< member_attendance >────────────── matches
                         member_id                      match_id
                         match_id
```

### Core Tables

| Table | Grain | Purpose |
|---|---|---|
| `members` | One row per member | CRM and engagement attributes |
| `matches` | One row per AFL match | Fixture, score and attendance data |
| `member_attendance` | One member-match event | Match attendance bridge/fact table |
| `transactions` | One row per transaction | Commercial activity |
| `member_360` | One row per member | Aggregated reporting view |

A date dimension and integrity checks are also included in the SQL layer.

---

## SQL & Data Engineering

The SQL workflow demonstrates:

- Relational joins
- Aggregation
- CTEs
- `CASE` logic
- Window functions
- `COALESCE` and null handling
- Reporting views
- Date modelling
- Key-integrity testing
- Referential-integrity testing
- Data-quality checks
- Analytical exports

The `member_360` reporting layer consolidates CRM, attendance and transaction behaviour into a single member-level analytical view.

---

## Dashboard 1 — Member Intelligence

The first dashboard focuses on **member engagement, retention and commercial performance**.

Headline metrics:

- **5,000** simulated members
- **61.6%** simulated renewal rate
- **$128.79** average spend per member
- **4.8** average matches attended

Analysis includes:

- Renewal rate by membership tier
- Attendance and renewal
- Engagement and renewal
- Average member value by tier
- Revenue by transaction category
- Business interpretation and limitations

### Selected Findings

Higher membership tiers show stronger simulated renewal rates, with Premium members producing the highest renewal rate and average spend per member.

Simulated renewal also increases across higher match-attendance groups, illustrating how attendance behaviour could be incorporated into retention analysis.

Merchandise represents the largest simulated transaction-revenue category.

> These CRM findings arise from simulated data and should not be interpreted as real Richmond Football Club member behaviour or causal relationships.

---

## Dashboard 2 — Match & Fan Behaviour

The second dashboard connects the CRM case study to the **real 2025 Richmond home-match environment**.

Public-data metrics include:

- **12** Richmond home matches
- **41,534** average stadium attendance
- **80,009** highest home attendance
- **4** home wins

Analysis includes:

- Stadium attendance by opponent
- Home attendance through the season
- Match-result margins
- Match-level engagement profiling
- Integration of public fixture data with simulated CRM attendance

The dashboard also explicitly highlights a limitation of the synthetic model: simulated member attendance varies relatively little between opponents, while real stadium demand varies substantially.

This suggests that a more sophisticated attendance model could incorporate factors such as opponent attractiveness, fixture timing, venue characteristics and recent team performance.

---

## Data Validation

A dedicated validation script performs final project-level QA.

Checks include:

- Required data and dashboard files
- Database connectivity
- Member ID uniqueness
- Match ID uniqueness
- Duplicate member-match events
- Referential integrity
- Transaction totals
- Reporting-view row counts
- Invalid spend and attendance values
- Email engagement ranges
- Dashboard KPI reconciliation

The final validation run completed with **all checks passing**.

Run validation with:

```bash
python Python/validate_project.py
```

---

## Technology Stack

**Python**
- pandas
- NumPy
- Requests
- BeautifulSoup
- Plotly
- Streamlit

**Data & SQL**
- DuckDB
- SQL

**Development**
- VS Code
- Git
- GitHub

---

## Repository Structure

```text
football-fan-analytics/
│
├── Dashboard/
│   ├── app.py
│   └── pages/
│       └── Match_Fan_Behaviour.py
│
├── Data/
│   ├── Raw/
│   │   ├── afl_matches_2025.csv
│   │   ├── synthetic_members.csv
│   │   ├── synthetic_member_attendance.csv
│   │   └── synthetic_transactions.csv
│   │
│   ├── member_360.csv
│   ├── attendance_analysis.csv
│   └── transaction_analysis.csv
│
├── Python/
│   ├── extract_afl_data.py
│   ├── generate_synthetic_crm.py
│   ├── generate_member_attendance.py
│   ├── generate_transactions.py
│   ├── run_sql.py
│   └── validate_project.py
│
├── SQL/
│   └── 01–26 SQL workflow
│
├── football_analytics.duckdb
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Project

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run project validation

```bash
python Python/validate_project.py
```

### 4. Launch the dashboard

```bash
python -m streamlit run Dashboard/app.py
```

Streamlit will launch the Member Intelligence dashboard with navigation to the Match & Fan Behaviour page.

---

## Limitations

This project is designed to demonstrate an analytics workflow rather than reproduce a real football club's internal data environment.

Key limitations include:

- CRM, transaction and member-attendance data are simulated.
- Synthetic behavioural relationships were intentionally generated.
- The project uses DuckDB as a local analytical database rather than an enterprise cloud warehouse.
- Match-level simulated attendance does not strongly incorporate opponent-specific demand.
- Associations in simulated data should not be interpreted as causal findings.

These limitations are intentionally disclosed throughout the project and dashboards.

---

## Potential Extensions

With access to real club data, the analytical framework could be extended to:

- Renewal propensity modelling
- Member churn-risk scoring
- Campaign-response analysis
- Match-attendance forecasting
- Customer lifetime value
- Member segmentation
- Ticket-demand modelling
- Marketing attribution
- Automated data-quality monitoring

---

## Data Disclosure

This is an independent portfolio project using publicly available AFL match data from AFL Tables and simulated CRM/member data.

**No proprietary Richmond Football Club data is used.**

Simulated relationships are illustrative and should not be interpreted as findings about actual Richmond members.