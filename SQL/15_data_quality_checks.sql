SELECT
    COUNT(*) AS total_rows,

    COUNT(DISTINCT member_id) AS unique_members,

    COUNT(*) - COUNT(DISTINCT member_id) AS duplicate_members,

    SUM(CASE WHEN member_id IS NULL THEN 1 ELSE 0 END)
        AS missing_member_ids,

    SUM(CASE WHEN matches_attended < 0 THEN 1 ELSE 0 END)
        AS invalid_attendance,

    SUM(CASE WHEN total_spend < 0 THEN 1 ELSE 0 END)
        AS invalid_spend,

    SUM(CASE WHEN email_open_rate < 0 OR email_open_rate > 1
        THEN 1 ELSE 0 END)
        AS invalid_email_open_rates

FROM member_360;