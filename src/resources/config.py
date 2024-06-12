import datetime
import os
""" /data/postgres/{table}/2024-01-01/file.format
/data/postgres/{table}/2024-01-02/file.format
/data/csv/2024-01-02/file.format
 """
# Organization of name of files
postgres = lambda table, date: f"data\\postgres\\{table}\\{date}" #extracao.parquet
csv = lambda date: f"data\\csv\\{date}" #extracao.parquet

print(datetime.date.today())
#path = postgres("orders", datetime.datetime(2024,6,9).date())

#os.makedirs(path, exist_ok=True)
# Organization of the paths to datalake

# Organization combo
