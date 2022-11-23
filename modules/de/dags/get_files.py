#from get_conn_string import get_conn_string
from sqlalchemy import create_engine
import psycopg2
import os



def get_file_from_s3(fname):
    """
    Read an s3 file into a Pandas dataframe.
    """
    import pandas as pd
    import boto3
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name='eu-west-1'
    )

    data = s3.get_object(
        Bucket='daredata-technical-challenge-data',
        Key=fname
    )
    data = pd.read_csv(data['Body'])

    return data



def s3_to_table(fname):
    """
    Reads an s3 file and creates a new table in the database with the contents of this file.
    """                  
    db_url = f"postgresql+psycopg2://{os.environ['ADMIN_DB_USER']}:{os.environ['ADMIN_DB_PASSWORD']}@localhost/companydata"
    engine = create_engine(db_url, convert_unicode=True, client_encoding='utf8')

    #engine = create_engine('postgresql+psycopg2://admin:admin@localhost/companydata')
    #connection = engine.connect()

    data = get_file_from_s3(fname)

    data.to_sql(
        fname.split('.csv')[0],
        con = engine,
        index=False,
        if_exists='replace'
    )

def get_prev_month_sales(**context):
    """Gets the sales for the current month, based on an Airflow DAG run.
    """
    db_url = f"postgresql+psycopg2://{os.environ['ADMIN_DB_USER']}:{os.environ['ADMIN_DB_PASSWORD']}@operational-db/companydata"
    engine = create_engine(db_url, convert_unicode=True, client_encoding='utf8')

    month = context["data_interval_start"].strftime("%Y-%m-%d")
   
# assumes credentials & configuration are handled outside python in .aws directory or environment variables    

    fname = f"sales/{month}/sales.csv"

    data = get_file_from_s3(fname=fname)

    data.to_sql(
        "sales",
        con = engine,
        index=False,
        if_exists='append'
    )
