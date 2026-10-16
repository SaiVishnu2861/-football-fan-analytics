CREATE OR REPLACE TABLE transactions AS
SELECT *
FROM read_csv_auto('Data/Raw/synthetic_transactions.csv');