CREATE OR REPLACE VIEW member_360 AS

WITH attendance_summary AS (

    SELECT
        member_id,
        COUNT(DISTINCT match_id) AS matches_attended

    FROM member_attendance

    GROUP BY member_id
),

transaction_summary AS (

    SELECT
        member_id,
        COUNT(transaction_id) AS transaction_count,
        ROUND(SUM(amount), 2) AS total_spend,
        ROUND(AVG(amount), 2) AS avg_transaction_value

    FROM transactions

    GROUP BY member_id
)

SELECT
    m.member_id,
    m.age,
    m.region,
    m.membership_tier,
    m.years_as_member,
    m.join_year,
    m.auto_renew,

    m.emails_sent,
    m.emails_opened,
    m.email_clicks,
    m.app_sessions,

    ROUND(
        m.emails_opened * 1.0 / NULLIF(m.emails_sent, 0),
        3
    ) AS email_open_rate,

    COALESCE(
        a.matches_attended,
        0
    ) AS matches_attended,

    COALESCE(
        t.transaction_count,
        0
    ) AS transaction_count,

    COALESCE(
        t.total_spend,
        0
    ) AS total_spend,

    COALESCE(
        t.avg_transaction_value,
        0
    ) AS avg_transaction_value,

    m.renewed_2026

FROM members AS m

LEFT JOIN attendance_summary AS a
    ON m.member_id = a.member_id

LEFT JOIN transaction_summary AS t
    ON m.member_id = t.member_id;