SELECT
    m.membership_tier,

    COUNT(DISTINCT m.member_id) AS members,

    COUNT(t.transaction_id) AS transactions,

    ROUND(
        SUM(t.amount),
        2
    ) AS total_revenue,

    ROUND(
        SUM(t.amount) / COUNT(DISTINCT m.member_id),
        2
    ) AS revenue_per_member

FROM members AS m

LEFT JOIN transactions AS t
    ON m.member_id = t.member_id

GROUP BY
    m.membership_tier

ORDER BY
    revenue_per_member DESC;