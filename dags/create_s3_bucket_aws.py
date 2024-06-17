from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sensors.external_task import ExternalTaskSensor


with DAG(
   dag_id="create_s3_bucket_aws",
   start_date=datetime(2024, 6, 7, 12, 0, 0),
   schedule_interval="0 12 * * *",
   catchup=True,
   max_active_runs=1,
) as dag:
   sleep = BashOperator(
      task_id = "sleep",
      bash_command="sleep 40"
   )
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
      bash_command="aws --endpoint-url=http://localstack:4566 s3 cp /opt/airflow/data_provided/order_details.csv  s3://test/order_details-{{ ds }}.csv"
   )

   
   sleep>>task1>>task2>>task3
   
