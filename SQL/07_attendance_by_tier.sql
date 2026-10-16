SELECT
    m.membership_tier,
    COUNT(*) AS total_attendances,
    COUNT(DISTINCT ma.member_id) AS unique_attendees,
    ROUND(
        COUNT(*) * 1.0 / COUNT(DISTINCT ma.member_id),
        2
    ) AS avg_matches_per_attendee
FROM member_attendance AS ma

JOIN members AS m
    ON ma.member_id = m.member_id

GROUP BY m.membership_tier

ORDER BY avg_matches_per_attendee DESC;