-- --------------------------------------------------
-- KEY & REFERENTIAL INTEGRITY CHECKS
-- A healthy model should return 0 for every check.
-- --------------------------------------------------

SELECT
    'duplicate_member_ids' AS check_name,
    COUNT(*) - COUNT(DISTINCT member_id) AS issue_count
FROM members

UNION ALL

SELECT
    'duplicate_match_ids' AS check_name,
    COUNT(*) - COUNT(DISTINCT match_id) AS issue_count
FROM matches

UNION ALL

SELECT
    'duplicate_transaction_ids' AS check_name,
    COUNT(*) - COUNT(DISTINCT transaction_id) AS issue_count
FROM transactions

UNION ALL

SELECT
    'duplicate_attendance_pairs' AS check_name,
    COUNT(*) - COUNT(DISTINCT (member_id, match_id)) AS issue_count
FROM member_attendance

UNION ALL

SELECT
    'orphan_transaction_members' AS check_name,
    COUNT(*) AS issue_count
FROM transactions AS t
LEFT JOIN members AS m
    ON t.member_id = m.member_id
WHERE m.member_id IS NULL

UNION ALL

SELECT
    'orphan_attendance_members' AS check_name,
    COUNT(*) AS issue_count
FROM member_attendance AS ma
LEFT JOIN members AS m
    ON ma.member_id = m.member_id
WHERE m.member_id IS NULL

UNION ALL

SELECT
    'orphan_attendance_matches' AS check_name,
    COUNT(*) AS issue_count
FROM member_attendance AS ma
LEFT JOIN matches AS mt
    ON ma.match_id = mt.match_id
WHERE mt.match_id IS NULL;