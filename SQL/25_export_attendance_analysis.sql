COPY (
    SELECT
        ma.member_id,
        ma.match_id,

        -- Member attributes
        m.membership_tier,
        m.years_as_member,
        m.region,
        m.renewed_2026,

        -- Match attributes
        mt.match_date,
        mt.home_team,
        mt.away_team,
        mt.venue,
        mt.attendance AS total_match_attendance,

        -- Calendar attributes
        d.month_number,
        d.month_name,
        d.quarter,
        d.day_name,
        d.is_weekend

    FROM member_attendance AS ma

    JOIN members AS m
        ON ma.member_id = m.member_id

    JOIN matches AS mt
        ON ma.match_id = mt.match_id

    JOIN dim_date AS d
        ON mt.match_date = d.date
)
TO 'Data/attendance_analysis.csv'
WITH (
    HEADER TRUE,
    DELIMITER ','
);