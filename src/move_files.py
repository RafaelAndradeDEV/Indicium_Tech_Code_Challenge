import os
import datetime
import shutil

source_path_csv = os.path.join(os.getcwd(),f'data/order_details.csv')
destination_path_csv = os.path.join(os.getcwd(),f'data/csv/{datetime.date.today()}')  # Altere conforme necessário
os.makedirs(destination_path_csv, exist_ok=True)
shutil.move(source_path_csv, destination_path_csv)

source_path_postgres = os.path.join(os.getcwd(),f'data/')
files = os.listdir(source_path_postgres)
files = [file for file in files if file.endswith(".csv")]
files_renamed = [file.split("-")[1] for file in files if file.endswith(".csv")]
for file, file_renamed in zip(files, files_renamed):
   os.rename(source_path_postgres+file, source_path_postgres+file_renamed)
for table in files_renamed:
   source_path_postgres_file = os.path.join(os.getcwd(),f'data/{table}')
   destination_path_postgres = os.path.join(os.getcwd(),f'data/postgres/{table[:-4]}/{datetime.date.today()}')
   os.makedirs(destination_path_postgres, exist_ok=True)
   shutil.move(source_path_postgres_file, destination_path_postgres) 

