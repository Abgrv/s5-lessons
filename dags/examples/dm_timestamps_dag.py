from datetime import datetime
from airflow import DAG

#from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
import json
import pandas as pd

from lib.dict_util import json2str
from lib.dict_util import str2json
 
# Параметры подключения к БД Postgres
PG_CONN_ID = "PG_WAREHOUSE_CONNECTION"

 
def read_data_from_stg():
    pg_hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    
    query = """
    INSERT INTO dds.dm_timestamps (ts,	"year", "month", "day", "date", "time")
        SELECT 
        (object_value::JSON->>'date')::timestamp AS ts,
        EXTRACT(YEAR  FROM (object_value::JSON->>'date')::timestamp)::int AS "year",
        EXTRACT(MONTH FROM (object_value::JSON->>'date')::timestamp)::int AS "month",
        EXTRACT(DAY   FROM (object_value::JSON->>'date')::timestamp)::int AS "day",
        (object_value::JSON->>'date')::date AS "date",
        (object_value::JSON->>'date')::time AS "time"
    FROM stg.ordersystem_orders AS oo 
    ;
    """
    cursor.execute(query)

    connection.commit()
    connection.close()

    return 300

# Создание DAG
with DAG(
    "stg_to_dds_timestamps_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
read_data 