# Use the official Apache Airflow image as a base
FROM apache/airflow:2.9.1

# Install system dependencies required to install the AWS CLI
USER root
RUN apt-get update && \
    apt-get install -y curl unzip gcc g++ python3-dev && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --assume-yes git


# Create a virtual environment to run meltano
RUN python -m venv /venv-meltano
ENV PATH="/venv-meltano/bin:${PATH}"
    
# Install Meltano in the virtual environment
RUN pip install meltano
RUN pip install --upgrade setuptools


# Switch back to airflow user
USER airflow

#Copy the folders from the directory to the container and install the plugins
COPY . .
ADD .env /opt/airflow/.env
RUN meltano install

RUN /bin/bash -c "source /opt/airflow/.meltano/loaders/target-csv/venv/bin/activate && pip install setuptools"


