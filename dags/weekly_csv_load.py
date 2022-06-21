docs = """
## Weekly CSV Load

#### Purpose

DAG to download the CSV file with the updated data
to then clean and load this data to our db.

#### Outputs

This pipeline create new registers without duplicates
from the downloaded csv files into the SLQ Server - 
`dbo.Unificado` table.

#### Owner

For any questions or concerns, please contact
[marianoreinfo@gmail.com](mailto:marianoreinfo@gmail.com).

"""
from datetime import datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from project.cfg import SQL_SERVER_CFG
from project.constants import CSV_URL
from project.extract import download_csv_file
from project.helpers import format_temp_files
from project.load import mount_db_backup
from project.main import load_dfs

default_args = {"owner": "marianore", "start_date": datetime(2022, 1, 1)}

dag = DAG(
    dag_id="weekly_csv_load_dag",
    default_args=default_args,
    catchup=False,
    schedule_interval="0 5 * * 1",
    doc_md=docs,
)

start_task = DummyOperator(task_id="start")

mount_db_backup_task = PythonOperator(
    task_id="mount_db_backup", python_callable=mount_db_backup, op_args=[SQL_SERVER_CFG]
)

format_temp_files_task = PythonOperator(
    task_id="format_temp_files",
    python_callable=format_temp_files,
)

download_csv_file_task = PythonOperator(
    task_id="download_csv_file",
    python_callable=download_csv_file,
    op_args=[CSV_URL],
)

load_df_task = PythonOperator(
    task_id="load_df",
    python_callable=load_dfs,
)

end_task = DummyOperator(task_id="end")

(
    start_task
    >> mount_db_backup_task
    >> format_temp_files_task
    >> download_csv_file_task
    >> load_df_task
    >> end_task
)
