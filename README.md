# Indicium_Tech_Code_Challenge
O desafio foi desenvolver uma pipeline de extração de dados(csv, postgres) e ingestão em um banco de dados(postgres)

#### Ideia proposta para solução:
**1° etapa:** Armazenamento: Criação de 2 bancos de dados postgres, um para armazenamento dos dados fornecidos e outro para ingestão de dados extraídos, simulando um ambiente em que temos Data Source com criação diária de dados e um ambiente de preparação para futuro armazenamento em DW e utilização em ferramentas de BI. Foi pensado também em um local ideal para armazenamento do arquivo csv: "order_details", o serviço S3 bucket foi o que melhor se ajustou para o problema, pensando em um ambiente de produção onde há escalabilidade, baixo custo, facilidade de acesso e integração.

**2° etapa:** Configuração `dockerfile` e `docker-compose` para criação de imagens para cada banco proposto e ajustes em outros módulos para perfeito execução dentro do contêiner. Criação de Utils(localizado em `/src`) para ajudar na execução e solução do problema

**3° etapa:** Criação de DAG's: O objetivo inicial foi criar 3 dag's: Ingestão do arquivo csv no bucket, pipeline de extração de ambos ambientes(postgres e bucket) e pipeline de ingestão no ambiente(postgres). 2 dag's(extração e ingestão) não foi possível concluir à tempo, visto a difícil integração no contêiner(erro de módulo, conexão com banco de dados e instalação de plugins), mas foi desenvolvido para rodar localmente com exatidão.

**4° etapa:** Documentação e busca por melhoria de processos.

## Passos de instalação:
### **Clonagem do repositório da aplicação**

`git clone https://github.com/RafaelAndradeDEV/Indicium_Tech_Code_Challenge.git`

`cd Indicium_Tech_Code_Challenge`

### **Instalação dependências(executar no bash):**

`poetry install`

`poetry shell`

`meltano install`

OBS: Foi criado um arquivo .env para armazenamento de váriaveis confidenciais(para conexão com banco de dados) e de uso interno de scripts. Dentre elas: DATA_PATH = ${PWD}

Tendo instalado as dependências e plugins do meltano, podemos iniciar o nosso contêiner com as imagens dos bancos de dados e airflow.

### **Execução projeto:**

`docker-compose airflow-init`

`docker-compose up`

Assim que o contêiner estiver funcionando, será executada uma dag para criação de um Bucket no S3, criado localmente, para armazenamento do arquivo `order_details.csv`, simulando um ambiente padrão de extração de dados. Para verificar se ela foi aciona, acesse:

`http://localhost:8081/home`

**Usuário: airflow**

**senha: ariflow**

Caso não tenha sido acionada basta aciona-lá:

![image](/docs/acionar_dag.png)

É necessário também ajustar path's dentro do arquivo `files_def.json`, para posterior utilização pelo serviço do meltano plugin, por isso execute:

`python src/change_path_json.py`

Tudo ajustado e pronto, podemos começar com a execução dos plugins fornecidos pelo meltano:

#### Extração:

`meltano run tap-s3-csv target-csv`

`meltano run tap-postgres target-csv`

No processo de configuração os arquivos ficam com metadados relacionados à datas(ex: order_details-20240612T155529.csv), para retirada destes metadados, execute:

`python src/rename_files.py`

#### Ingestão:

`meltano run tap-csv target-postgres`

Feito esse último processo, podemos organizar os arquivos capturados por meio do seguinte script:

`python src/move_files.py`

#### Estrutura de diretório e arquivos:
```

Indicium_Tech_Code_Challenge/
├── config/
│   └── airflow.cfg
├── dags/
│   └── create_s3_bucket_aws.py
├── data/
│   ├── csv/
│   └── postgres/
├── data_provided/
│   ├── northwind.sql
│   └── order_details.csv
├── data_provided/
│   ├── northwind.sql
│   └── order_details.csv
├── plugins/
│   ├── extractors/
│   └── loaders/
├── query/
│   └── result.sql
├── query_result/
│   └── query_result.csv
├── src/
│   ├── resources/
│   │   └── __pycache__/
│   ├── config.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── __init__.cpython-39.pyc
│   ├── change_path_json.py
│   ├── move_files.py
│   └── rename_files.py
├── LICENSE     
├── code_challenge.md
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile  README.md  
├── files_def.json  
├── meltano.yml  
├── poetry.lock  
└── requirements.txt
```

### Insights
### Desafios & dificuldades & opinião do desafio



