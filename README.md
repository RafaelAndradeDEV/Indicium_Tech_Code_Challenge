# Indicium_Tech_Code_Challenge

Descrição do code_challenge: [LINK](/code_challenge.md)

Autor: Rafael Andrade

Breve Introdução: O desafio foi desenvolver uma pipeline de extração de dados(csv, postgres) e ingestão em um banco de dados(postgres), utilizando Airflow para orchestração e Meltano para Extract e Load.

## Tabela de conteúdos:
1. [Ideia proposta para solução](#Ideia-proposta-para-solução)
2. [Passos de instalação](#Passos-de-instalação)
   * [Clonagem do repositório da aplicação](#clonagem-do-repositório-da-aplicação)
   * [Instalação de dependências](#instalação-de-dependênciasexecutar-no-bash)
3. [Execução projeto](#execução-projeto)
   * [Credenciais para login](#credenciais-para-login)
   * [Regras implementadas nas Dags](#regras-implementadas-nas-dags)
4. [Resultados](#resultados)
5. [Estrutura de diretório e arquivos](#estrutura-de-diretório-e-arquivos)
6. [Detalhes de implementação](#detalhes-de-implementação)
7. [Insights](#insights)
8. [Desafios & dificuldades & opinião do desafio](#desafios--dificuldades--opinião-do-desafio)

## Ideia proposta para solução:
**1° etapa:** Armazenamento: Criação de 2 bancos de dados postgres, um para armazenamento dos dados fornecidos e outro para ingestão de dados extraídos, simulando um ambiente em que temos Data Source com criação diária de dados e um ambiente de preparação para futuro armazenamento em DW e utilização em ferramentas de BI. Foi pensado também em um local ideal para armazenamento do arquivo csv: "order_details", o serviço S3 bucket foi o que melhor se ajustou para o problema, pensando em um ambiente de produção onde há escalabilidade, baixo custo, facilidade de acesso e integração.

**2° etapa:** Configuração `dockerfile` e `docker-compose` para criação de imagens para cada banco proposto e ajustes em outros módulos para perfeito execução dentro do contêiner. Criação de Utils(localizado em `./src`) para ajudar na execução e solução do problema. Criação do projeto meltano para ajustes de configuração e instalação de plugins.

**3° etapa:** Criação de DAG's: Foram feitas 3 dag's: 
- create_s3_bucket_aws: Responsável pela:
   - criação do bucket no S3 AWS via localstack instalado no docker-compose 
   - envio de arquivos `order_details-{date_execution_dag}.csv`, simulando ingestões feitas pelo negócio
- stage1: Executar comandos de extração e ajustes: 
   - Postgres(Data Source) -> local filesystem
   - Bucket S3(Data Source) -> local filesystem
   - Ajustar nomes dos arquivos provindos da extração(São gravados no processo de escrita dos arquivos com metadado relacionado a data da captura)
   - Renomear paths dentro do arquivo de configuração: `files_def.json`
- stage2: Executar comandos de load e organização das pastas:
   - local filesystem -> Postgres
   - Organizar arquivos a partir da data em que foram capturados

**4° etapa:** Documentação e busca por melhoria de processos.

## Passos de instalação:
### **nota:**
- **É assumido que o docker já esteja devidamente instalado**
- **Projeto desenvolvido em ambiente linux**

### **Clonagem do repositório da aplicação**

```
git clone https://github.com/RafaelAndradeDEV/Indicium_Tech_Code_Challenge.git
cd Indicium_Tech_Code_Challenge
```

### **Instalação de dependências(executar no bash):**
Instalar dependência "Meltano" no projeto utilizando [Poetry](https://python-poetry.org/docs/) (Gerenciador de pacotes e ambientes virtuais):
```
poetry install
```
Ativação do ambiente virtual:
```
poetry shell
```
Ambiente ativado, podemos prosseguir com a instalação dos pluguins utilizado no projeto:
```
meltano install
```

OBS: Foi criado um arquivo .env para armazenamento de váriaveis sensíveis(utilizadas na conexão com banco de dados, bucket AWS) e de uso interno dos scripts.

Tendo instalado as dependências e plugins do meltano, podemos iniciar o nosso contêiner com as imagens dos bancos de dados e airflow.

## **Execução projeto:**

Construção das imagens:
```
docker-compose build
```
Inicialização dos contêineres:
```
docker-compose up
```

Quando o contêiner estiver ativo, você vai poder acessar o webserver do airflow pela URL:

`http://localhost:8081/home`

### Credenciais para login:
- **Usuário: airflow**

- **senha: airflow**

![image](/docs/dags.png)

### Regras implementadas nas Dags:
   - Execução diária às 12:00
   - É possível executar todos os dias anteriores até o dia atual, utilizando data de início configura nela
   - Stage1 e Stage2 são independentes entre si
   - Stage2 não é acionada no dia em que o Stage1 não for executado ou falhar


---
## Resultados:

**Pastas geradas(csv):** [pasta_csv](/data/csv/)

**Pastas geradas(postgres):** [pasta_postgres](/data/postgres/)

**Query utilizada:** [query](/query/result.sql)

**Resultado da query proposta ao final do desafio:** [resultado](/query_result/query_result.csv)

---




## Estrutura de diretório e arquivos:
```

Indicium_Tech_Code_Challenge/
├── .meltano/
├── config/
│   └── airflow.cfg
├── dags/
│   ├── stage1.py
│   ├── stage2.py
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
├── docs/
│   ├── dags.png
│   └── diagrama_embulk_meltanoo.jpg
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
├── .gitignore
├── .dockerignore
├── LICENSE     
├── code_challenge.md
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile  
├── README.md  
├── files_def.json  
├── meltano.yml  
├── poetry.lock  
└── requirements.txt
```

## Detalhes de implementação:

Foi adotado no projeto a escrita dos dados no formato `.csv`, devido:
   - Simplicidade: Simples de criar e entender
   - Legibilidade: podem ser facilmente lidos e editados com qualquer editor de texto
   - Portabilidade: É suportado por várias ferramentas de software, incluindo programas de planilhas (como Excel), bancos de dados, linguagens de programação e sistemas de gerenciamento de dados.
   - Para conjuntos de dados pequenos a moderados, o desempenho de leitura e escrita de arquivos CSV pode ser suficientemente rápido e eficiente.

OBS: Dependendo da quantidade de dados que será trafegado, o `.csv` pode se tornar custoso e demorado, uma ideia seria utilizar o formato `.parquet` para melhorar a eficiência na mobilidade dos dados, menos tráfego de dados = menos gastos(de processamento e armazenamento).

### Foram utilizados 5 plugins:
#### Extractors:
- #### tap-s3-csv: Buscar no S3, arquivos `.csv`
   config:
   ```
   variant: transferwise
   pip_url: pipelinewise-tap-s3-csv
   config:
      aws_profile: ''
      bucket: test
      start_date: '2024-06-05T00:00:00Z'
      tables: [{search_prefix: '', search_pattern: .csv, table_name: order_details, delimiter: ',', key_properties: [order_id]}]
      metadata:
      '*':
        replication-method: INCREMENTAL
        replication-key: id
   ```
- #### tap-postgres: Extrair todas tabelas do banco Postgres
   config:
   ``` 
   variant: meltanolabs
   pip_url: git+https://github.com/MeltanoLabs/tap-postgres.git
   config:
      database: northwind
      host: postgres_db2
      port: 5432
      sqlalchemy_url: postgresql://northwind_user:thewindisblowing@postgres_db2:5432/northwind
      user: northwind_user
      default_replication_method: INCREMENTAL
      filter_schemas:
         - public
   ```
- #### tap-csv: Busca arquivos `.csv` localmente
   config:
   ``` 
   variant: meltanolabs
   pip_url: git+https://github.com/MeltanoLabs/tap-csv.git
   config:
      csv_files_definition: ${PWD}/files_def.json
      add_metadata_columns: false
   ```
#### loaders:
- #### target-csv: Grava localmente os arquivos `.csv` capturas pelos pluguins de extração
   config:
   ``` 
   variant: hotgluexyz
   pip_url: git+https://github.com/hotgluexyz/target-csv.git
   config:
      destination_path: ${PWD}/data
   ```
- #### target-postgres: Faz a ingestão de dados no Postgres
   config: 
   ``` 
   variant: meltanolabs
   pip_url: meltanolabs-target-postgres
   config:
      activate_version: false
      add_record_metadata: false
      database: final_db
      host: postgres_db3
      port: 5434
      sqlalchemy_url: postgresql://rafael:rafaeldev@postgres_db3:5432/final_db
      user: rafael
   ```
   
#### Execuções dos plugins nas Dags:

Stage1:
   - meltano run tap-s3-csv target-csv
   - meltano run tap-postgres target-csv

Stage2:
   - meltano run tap-csv target-postgres


## Insights:

A escolha do meltano como extrator, transformer e loader é interessante visto a facilidade de desenvolvimento e automação de comandos, ainda não muito utilizado no mercado, mas demonstra ótimas soluções com um bom tempo de entrega dos resultados. Em geral, uma boa ferramenta para soluções rápidas. 

## Desafios & dificuldades & opinião do desafio:

Desafio muito interessante, foram aplicados diversos conhecimentos relacionado a pipelines, processos, conteinerização, conexões com fontes de dados e pensamento analítico, utilizando Python, Bash, SQL, Airflow, Docker, Meltano. 

A maior dificuldade foi implementar uma nova ferramenta ao airflow, buscando à automação via DAG. Parte da documentação no site do [Meltano](https://meltano.com/) ajudou na implementação dessa solução, mas houve muitos problemas no caminho que foram solucionados a partir de logs.


