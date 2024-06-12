import os
import json
from dotenv import load_dotenv

# Carregar o valor da variável de ambiente
load_dotenv()
data_path = os.environ.get("DATA_PATH")

# Caminho para o arquivo JSON
json_file_path = os.path.join(data_path,'files_def.json')

# Carregar o JSON
with open(json_file_path, 'r') as file:
   data = json.load(file)

# Atualizar os caminhos no JSON
   for entry in data:
      entry['path'] = entry['path'].replace('/mnt/c/GitHub/meltano', data_path)

# Salvar o JSON atualizado
with open(json_file_path, 'w') as file:
    json.dump(data, file, indent=2)

print(f"Updated paths in {json_file_path}")


# List buckets:
#aws s3 ls --endpoint-url http://localhost:4566 --recursive --human-readable

#aws s3 mb s3://my-bucket --endpoint-url http://localhost:4566
#aws configure list

# Create Bucket
#aws --endpoint-url=http://localhost:4566 s3 mb s3://test

# Bucket ACL
#aws --endpoint-url=http://localhost:4566 s3api put-bucket-acl --bucket test --acl public-read

# Copy to Bucket
#aws --endpoint-url=http://localhost:4566 s3 cp /tmp/test.tar  s3://test-bucket/test.tar

# ls bucket
# aws --endpoint-url=http://localhost:4566 s3 ls s3://test/

# Download
#aws --endpoint-url http://localhost:4566 s3 cp s3://test/order_details.csv C:/Github/meltano

