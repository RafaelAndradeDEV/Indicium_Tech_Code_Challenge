# Use a imagem oficial do Apache Airflow como base
FROM apache/airflow:2.9.1

# Instale dependências do sistema necessárias para instalar a AWS CLI
USER root
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --assume-yes git

RUN python -m venv /venv-meltano
ENV PATH="/venv-meltano/bin:${PATH}"
    
# Instale o Meltano no ambiente virtual
RUN pip install meltano

# Mude de volta para o usuário airflow
USER airflow

