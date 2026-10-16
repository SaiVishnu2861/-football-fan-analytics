SELECT
    'match_dates_missing_from_calendar' AS check_name,
    COUNT(*) AS issue_count
FROM matches AS m
LEFT JOIN dim_date AS d
    ON m.match_date = d.date
WHERE d.date IS NULL

UNION ALL

SELECT
    'transaction_dates_missing_from_calendar' AS check_name,
    COUNT(*) AS issue_count
FROM transactions AS t
LEFT JOIN dim_date AS d
    ON t.transaction_date = d.date
WHERE d.date IS NULL;