SELECT
    m.member_id,
    m.membership_tier,
    m.years_as_member,
    m.renewed_2026,
    COUNT(ma.match_id) AS matches_attended

FROM members AS m

LEFT JOIN member_attendance AS ma
    ON m.member_id = ma.member_id

GROUP BY
    m.member_id,
    m.membership_tier,
    m.years_as_member,
    m.renewed_2026

ORDER BY matches_attended DESC;