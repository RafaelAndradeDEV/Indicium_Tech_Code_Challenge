import os
import re

# Directory where the files are located
directory = os.path.join(os.getcwd(),'data/') 

# Regex pattern for files with order_details-YYYYMMDDTHHMMSS.csv format
pattern = re.compile(r'^(.*)-\d{8}T\d{6}\.csv$')

for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        # Extract the prefix (before timestamp)
        prefix = match.group(1)
        
        # Create new file name
        new_name = f"{prefix}.csv"
        
        # Full file paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)
        
        # Rename file
        os.rename(old_file, new_file)
        
        print(f"File '{filename}' renamed to '{new_name}'.")

print("All matching files have been renamed.")

