import os
import datetime
import shutil
import sys

# Takes argumente from dag 
execution_date = sys.argv[1]

# Identification of the csv file coming from the bucket, creates a folder according to the rule and moves the file
source_path_csv = os.path.join(os.getcwd(),f'data/order_details.csv')
destination_path_csv = os.path.join(os.getcwd(),f'data/csv/{execution_date}')  
os.makedirs(destination_path_csv, exist_ok=True)
shutil.move(source_path_csv, destination_path_csv)

# Identification of csv files coming from the database, creates a folder according to the rule and moves the files
source_path_postgres = os.path.join(os.getcwd(),f'data/')
files = os.listdir(source_path_postgres)
files = [file for file in files if file.endswith(".csv")]
files_renamed = [file.split("-")[1] for file in files if file.endswith(".csv")]

for file, file_renamed in zip(files, files_renamed):
   os.rename(source_path_postgres+file, source_path_postgres+file_renamed)

for table in files_renamed:
   source_path_postgres_file = os.path.join(os.getcwd(),f'data/{table}')
   destination_path_postgres = os.path.join(os.getcwd(),f'data/postgres/{table[:-4]}/{execution_date}')
   os.makedirs(destination_path_postgres, exist_ok=True)
   shutil.move(source_path_postgres_file, destination_path_postgres) 

