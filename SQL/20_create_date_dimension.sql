CREATE OR REPLACE TABLE dim_date AS

SELECT
    calendar_date AS date,

    YEAR(calendar_date) AS year,

    MONTH(calendar_date) AS month_number,

    MONTHNAME(calendar_date) AS month_name,

    QUARTER(calendar_date) AS quarter,

    DAY(calendar_date) AS day_of_month,

    DAYOFWEEK(calendar_date) AS day_of_week_number,

    DAYNAME(calendar_date) AS day_name,

    CASE
        WHEN DAYOFWEEK(calendar_date) IN (0, 6)
            THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM generate_series(
    DATE '2025-01-01',
    DATE '2025-12-31',
    INTERVAL 1 DAY
) AS dates(calendar_date);