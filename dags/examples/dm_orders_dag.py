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
    INSERT INTO dds.dm_orders(order_key, order_status, restaurant_id, timestamp_id, user_id)
    SELECT
        (oo.object_value::json->>'_id')                     AS order_key,
        (oo.object_value::json->>'final_status')            AS order_status,
        dr.id AS restaurant_id,
        dt.id AS timestamp_id,
        du.id AS user_id
    FROM stg.ordersystem_orders  AS oo
    INNER JOIN dds.dm_restaurants AS dr ON (oo.object_value::json->>'restaurant')::json->>'id' = dr.restaurant_id 
    INNER JOIN dds.dm_timestamps  AS dt ON (oo.object_value::json->>'update_ts')::timestamp    = dt.ts
    INNER JOIN dds.dm_users       AS du ON (oo.object_value::json->>'user')::json->>'id'       = du.user_id 
    ;
    """
    cursor.execute(query)

    connection.commit()
    connection.close()

    return 300

# Создание DAG
with DAG(
    "stg_to_dds_orders_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
read_data 