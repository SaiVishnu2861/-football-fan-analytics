SELECT
    home_team,
    COUNT(*) AS home_matches,
    ROUND(AVG(attendance), 0) AS average_attendance
FROM read_csv_auto('Data/Raw/afl_matches_2025.csv')
GROUP BY home_team
ORDER BY average_attendance DESC;
