import duckdb
import sys

sql_file = sys.argv[1]

with open(sql_file, "r") as file:
    query = file.read()

connection = duckdb.connect("football_analytics.duckdb")

result = connection.sql(query)

print(result)

connection.close()