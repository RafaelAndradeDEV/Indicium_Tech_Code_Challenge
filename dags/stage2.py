from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.sensors.external_task import ExternalTaskSensor


with DAG(
   dag_id="stage2",
   start_date=datetime(2024, 6, 7, 12, 0, 0),
   schedule_interval="0 12 * * *",
   catchup=True,
   max_active_runs=1,
) as dag:
   wait_for_stage1 = ExternalTaskSensor(
      task_id='wait_for_stage1',
      external_dag_id='stage1',
      external_task_id='fix_path_json',  
      allowed_states=['success'],
      execution_delta=timedelta(minutes=0), 
      mode='poke',  
      timeout=200, 
      poke_interval=5,
      dag=dag,
   )

   task1 = BashOperator(
      task_id = "csv_to_postgres",
      bash_command="cd /opt/airflow && meltano run tap-csv target-postgres"
   )
   task2 = BashOperator(
      task_id = "move_files",
      bash_command="cd /opt/airflow && python src/move_files.py {{ ds }}" # macro from airflow to execution date, format: YYYY-MM-DD
   )
   


   wait_for_stage1 >> task1 >> task2


