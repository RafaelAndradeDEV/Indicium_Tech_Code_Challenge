import os
import re

# Diretório onde os arquivos estão localizados
directory = os.path.join(os.getcwd(),'data/')  # Altere conforme necessário
print(directory)
# Padrão regex para arquivos com formato order_details-YYYYMMDDTHHMMSS.csv
pattern = re.compile(r'^(.*)-\d{8}T\d{6}\.csv$')

# Itera sobre cada arquivo no diretório
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        # Extrai o prefixo (antes do timestamp)
        prefix = match.group(1)
        
        # Cria o novo nome de arquivo
        new_name = f"{prefix}.csv"
        
        # Caminhos completos dos arquivos
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)
        
        # Renomeia o arquivo
        os.rename(old_file, new_file)
        
        print(f"Arquivo '{filename}' renomeado para '{new_name}'.")

print("Todos os arquivos correspondentes foram renomeados.")

