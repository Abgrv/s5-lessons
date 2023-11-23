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
    INSERT INTO dds.dm_products (restaurant_id, product_id, product_name, product_price, active_from, active_to)
    SELECT 
        id AS restaurant_id,
        (json_array_elements((object_value::json->>'menu')::json)::json->>'_id')::varchar AS product_id,
        (json_array_elements((object_value::json->>'menu')::json)::json->>'name')::text   AS product_name,
        (json_array_elements((object_value::json->>'menu')::json)::json->>'price')::numeric(14,2) AS product_price,
        (object_value::json->>'update_ts')::timestamp AS active_from,
        ('2099-12-31 00:00:00.000')::timestamp        AS active_to
    FROM stg.ordersystem_restaurants AS or2
    ORDER BY restaurant_id;
    """
    cursor.execute(query)

    connection.commit()
    connection.close()

    return 300

# Создание DAG
with DAG(
    "stg_to_dds_products_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
read_data 
