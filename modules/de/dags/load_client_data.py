import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from get_files import s3_to_table


def pg_hook(fname):
  data = s3_to_table("customer_activity.csv")
  print(data)
  postgres_sql_upload = PostgresHook(postgres_conn_id='operational_db', schema='companydata') 
  print(postgres_sql_upload)
  postgres_sql_upload.bulk_load("customer_activity", data)

with DAG(
    dag_id='load_client_data',
    catchup=False,
    start_date=datetime(2022, 1, 1)
) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print('Data load started.')
    )
    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print('Data load finished.')
    )

    # Loading base tables
    for fname in [
        "customer_activity.csv",
        "customer_profiles.csv",
        "labels.csv",
        "stores.csv"
    ]:
        
        load_file = PythonOperator(
            task_id=f'load_{fname}',
            python_callable=pg_hook,
            op_kwargs={"fname": fname}
        )

        start >> load_file >> end

