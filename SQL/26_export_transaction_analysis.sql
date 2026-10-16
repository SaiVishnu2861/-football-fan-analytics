COPY (
    SELECT
        t.transaction_id,
        t.member_id,

        -- Transaction attributes
        t.transaction_date,
        t.category,
        t.amount,

        -- Member attributes
        m.membership_tier,
        m.years_as_member,
        m.region,
        m.renewed_2026,

        -- Calendar attributes
        d.month_number,
        d.month_name,
        d.quarter,
        d.day_name,
        d.is_weekend

    FROM transactions AS t

    JOIN members AS m
        ON t.member_id = m.member_id

    JOIN dim_date AS d
        ON t.transaction_date = d.date
)
TO 'Data/transaction_analysis.csv'
WITH (
    HEADER TRUE,
    DELIMITER ','
);