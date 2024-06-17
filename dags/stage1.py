from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sensors.external_task import ExternalTaskSensor


with DAG(
   dag_id="stage1",
   start_date=datetime(2024, 6, 7, 12, 0, 0), #YYYY-mm-dd-HH-MM-SS
   schedule_interval="0 12 * * *",
   catchup=True,
   max_active_runs=1,
) as dag:
   wait_for_create_bucket = ExternalTaskSensor(
      task_id='wait_for_create_bucket',
      external_dag_id='create_s3_bucket_aws',
      external_task_id='send_archive', 
      allowed_states=['success'],
      execution_delta=timedelta(minutes=0),  
      mode='poke', 
      timeout=200,  
      poke_interval=5,
      dag=dag,
   )

   task1 = BashOperator(
      task_id = "s3_to_csv",
      bash_command="cd /opt/airflow && meltano run tap-s3-csv target-csv"
   )
   task2 = BashOperator(
      task_id = "postgres_to_csv",
      bash_command="cd /opt/airflow && meltano run tap-postgres target-csv"
   )
   task3 = BashOperator(
      task_id = "rename_files",
      bash_command="cd /opt/airflow && python src/rename_files.py"
   )
   task4 = BashOperator(
      task_id = "fix_path_json",
      bash_command="cd /opt/airflow && python src/change_path_json.py"
   )


   wait_for_create_bucket>>task1>>task2>>task3>>task4

