import os
import json
from dotenv import load_dotenv

try:
   # Load value from environment variables
   load_dotenv()
   data_path = os.environ.get("DATA_PATH")

   # Caminho para o arquivo JSON
   json_file_path = os.path.join(data_path,'files_def.json')

   # Path to JSON file
   with open(json_file_path, 'r') as file:
      data = json.load(file)
   # Update paths in JSON
      for entry in data:
         entry['path'] = entry['path'].replace("(data_path)", data_path)       

   # Save the updated JSON
   with open(json_file_path, 'w') as file:
      json.dump(data, file, indent=2)

   print(f"Updated paths in {json_file_path}")
except Exception as e:
   print("Already done or ERROR:", e)


