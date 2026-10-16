SELECT
    renewed_2026,

    COUNT(*) AS members,

    ROUND(
        AVG(matches_attended),
        2
    ) AS avg_matches_attended,

    ROUND(
        AVG(email_open_rate) * 100,
        1
    ) AS avg_email_open_rate_pct,

    ROUND(
        AVG(app_sessions),
        1
    ) AS avg_app_sessions,

    ROUND(
        AVG(transaction_count),
        2
    ) AS avg_transactions,

    ROUND(
        AVG(total_spend),
        2
    ) AS avg_total_spend,

    ROUND(
        AVG(years_as_member),
        1
    ) AS avg_tenure_years

FROM member_360

GROUP BY renewed_2026

ORDER BY renewed_2026 DESC;