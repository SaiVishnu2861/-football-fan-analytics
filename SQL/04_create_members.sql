CREATE OR REPLACE TABLE members AS
SELECT *
FROM read_csv_auto('Data/Raw/synthetic_members.csv');