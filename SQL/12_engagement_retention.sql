WITH member_engagement AS (

    SELECT
        member_id,
        renewed_2026,

        CASE
            WHEN emails_sent = 0 THEN 0
            ELSE emails_opened * 1.0 / emails_sent
        END AS email_open_rate,

        app_sessions

    FROM members
)

SELECT
    CASE
        WHEN email_open_rate < 0.30 THEN 'Low'
        WHEN email_open_rate < 0.60 THEN 'Medium'
        ELSE 'High'
    END AS engagement_segment,

    COUNT(*) AS members,

    ROUND(
        AVG(email_open_rate) * 100,
        1
    ) AS avg_email_open_rate_pct,

    ROUND(
        AVG(app_sessions),
        1
    ) AS avg_app_sessions,

    ROUND(
        AVG(CAST(renewed_2026 AS INTEGER)) * 100,
        1
    ) AS renewal_rate_pct

FROM member_engagement

GROUP BY engagement_segment

ORDER BY renewal_rate_pct DESC;