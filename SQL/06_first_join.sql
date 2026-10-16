SELECT
    ma.member_id,
    ma.match_id,
    m.membership_tier,
    m.years_as_member,
    mt.match_date,
    mt.away_team,
    mt.venue
FROM member_attendance AS ma

JOIN members AS m
    ON ma.member_id = m.member_id

JOIN matches AS mt
    ON ma.match_id = mt.match_id

LIMIT 20;