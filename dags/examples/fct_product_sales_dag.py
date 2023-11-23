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
    INSERT INTO dds.fct_product_sales(
        product_id,
        order_id,
        "count",
        price,
        total_sum,
        bonus_payment,
        bonus_grant
    )
    WITH 
    fct_ps AS (
    SELECT
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'product_id')::varchar           AS product_id,
        (be.event_value::json->>'order_id')::varchar                                                                  AS order_id,
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'quantity')::int                 AS "count",
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'price')::numeric(19, 5)         AS price,
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'product_cost')::numeric(19, 5)  AS total_sum,
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'bonus_payment')::numeric(19, 5) AS bonus_payment,
        (json_array_elements((event_value::json->>'product_payments')::json)::json->>'bonus_grant')::numeric(19, 5)   AS bonus_grant
    FROM stg.bonussystem_events AS be 
    WHERE event_type = 'bonus_transaction'
    )
    SELECT 
        dm_p.id              AS product_id,
        dm_o.id              AS order_id,
        fct_ps."count"       AS "count",
        fct_ps.price         AS price,
        fct_ps.total_sum     AS total_sum,
        fct_ps.bonus_payment AS bonus_payment,
        fct_ps.bonus_grant   AS bonus_grant
    FROM fct_ps
    INNER JOIN dds.dm_products AS dm_p ON fct_ps.product_id = dm_p.product_id 
    INNER JOIN dds.dm_orders   AS dm_o ON fct_ps.order_id = dm_o.order_key 
    ;
    """
    cursor.execute(query)

    connection.commit()
    connection.close()

    return 300

# Создание DAG
with DAG(
    "stg_to_dds_fct_product_sales_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
read_data 