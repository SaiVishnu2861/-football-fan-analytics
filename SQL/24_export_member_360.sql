COPY (
    SELECT *
    FROM member_360
)
TO 'Data/member_360.csv'
WITH (
    HEADER TRUE,
    DELIMITER ','
);