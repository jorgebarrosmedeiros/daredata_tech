import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator


with DAG(
    dag_id='statistical_results',
    start_date=datetime.datetime(2022, 1, 1),
    catchup=False,
) as dag:
    # Creating table with only the latest customer activity

    
    statistic = PostgresOperator(
        task_id="statistic_results",
        postgres_conn_id="operational_db",
        sql="sql/statistic_questions.sql",
    )
    
    # Start and end tasks
    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print('Data processing started.')
    )
    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print('Data processing finished.')
    )

    # Ordering tasks
    (
        start >> statistic >> end
    )
