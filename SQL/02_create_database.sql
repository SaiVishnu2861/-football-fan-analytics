CREATE OR REPLACE TABLE matches AS
SELECT
    ROW_NUMBER() OVER () AS match_id,
    STRPTIME(date, '%d-%b-%Y')::DATE AS match_date,
    time,
    home_team,
    away_team,
    home_score,
    away_score,
    attendance,
    venue
FROM read_csv_auto('Data/Raw/afl_matches_2025.csv');
