CREATE OR REPLACE TABLE member_attendance AS
SELECT *
FROM read_csv_auto('Data/Raw/synthetic_member_attendance.csv');