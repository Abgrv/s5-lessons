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
# PG_SCHEMA_STG = "stg"
# PG_SCHEMA_DDS = "dds"
 
def read_data_from_stg():
    pg_hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
 
    # Чтение данных из stg.bonussystem_user и stg.ordersystem_users
    cursor.execute("SELECT object_value FROM stg.ordersystem_users")
 
    result = cursor.fetchall()
    connection.close()
    
    temp_list = []

    for i in result:
        j = json.loads(i[0])
        temp_list.append(j)

    df = pd.DataFrame(temp_list)
    df = df.drop(columns=['update_ts'])
    


    connection = pg_hook.get_conn()
    cursor = connection.cursor()
 
    # Запись данных в базу
    
    insert_stmt = f"INSERT INTO dds.dm_users (user_id, user_name, user_login) VALUES (%s, %s, %s)"

    cursor.executemany(insert_stmt, df.values)
    connection.commit()
    connection.close()



    return result

# def transform_json_to_object(records):
#     transformed_records = []
#     for record in records:
#         obj = json.loads(record[2])
#         transformed_records.append((record[0], record[1], obj["_id"], obj["login"], obj["name"]))
#     return transformed_records
 
# def insert_records_to_dm_users(records):
#     pg_hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
#     connection = pg_hook.get_conn()
#     cursor = connection.cursor()
 
#     # Вставка объектов в dds.dm_users
#     insert_sql = f"INSERT INTO {PG_SCHEMA_DDS}.dm_users (id, user_id, user_name, user_login) VALUES (%s, %s, %s, %s)"
#     cursor.executemany(insert_sql, record)
#     connection.commit()
#     connection.close()



# Создание DAG
with DAG(
    "stg_to_dds_users_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
    # transform_json = PythonOperator(
    #     task_id="transform_json_to_object",
    #     python_callable=transform_json_to_object,
    #     op_kwargs={"records": "{{ ti.xcom_pull(task_ids='read_data_from_stg') }}"}
    # )
 
    # insert_to_dm_users = PythonOperator(
    #     task_id="insert_records_to_dm_users",
    #     python_callable=insert_records_to_dm_users,
    #     op_kwargs={"records": "{{ ti.xcom_pull(task_ids='transform_json_to_object') }}"}
    # )
 
read_data # >> transform_json >> insert_to_dm_users