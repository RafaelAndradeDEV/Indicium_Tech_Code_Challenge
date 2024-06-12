from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# docker run -it -v C:/Github:/project meltano/meltano init


with DAG(
   dag_id="dag_creation_bucket_s3",
   start_date=datetime(2024, 5,10),
   schedule_interval="@once",
   catchup=False,
) as dag:
   task1 = BashOperator(
      task_id = "create_bucket",
      bash_command="aws s3 mb s3://test --endpoint-url http://localstack:4566"
   )
   task2 = BashOperator(
      task_id = "config_public",
      bash_command="aws --endpoint-url=http://localstack:4566 s3api put-bucket-acl --bucket test --acl public-read"
   )
   task3 = BashOperator(
      task_id = "send_archive",
      bash_command="aws --endpoint-url=http://localstack:4566 s3 cp /opt/airflow/data_provided/order_details.csv  s3://test/order_details.csv"
   )

   
   task1>>task2>>task3
   
