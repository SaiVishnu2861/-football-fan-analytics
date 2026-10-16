WITH member_summary AS (

    SELECT
        m.member_id,
        m.renewed_2026,
        COUNT(ma.match_id) AS matches_attended

    FROM members AS m

    LEFT JOIN member_attendance AS ma
        ON m.member_id = ma.member_id

    GROUP BY
        m.member_id,
        m.renewed_2026
)

SELECT
    CASE
        WHEN matches_attended = 0 THEN '0 matches'
        WHEN matches_attended BETWEEN 1 AND 3 THEN '1-3 matches'
        WHEN matches_attended BETWEEN 4 AND 6 THEN '4-6 matches'
        WHEN matches_attended BETWEEN 7 AND 9 THEN '7-9 matches'
        ELSE '10+ matches'
    END AS attendance_group,

    COUNT(*) AS members,

    ROUND(
        AVG(CAST(renewed_2026 AS INTEGER)) * 100,
        1
    ) AS renewal_rate_pct

FROM member_summary

GROUP BY attendance_group

ORDER BY
    MIN(matches_attended);