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
 
    # Чтение данных из stg.bonussystem_user и stg.ordersystem_users
    cursor.execute("SELECT object_value FROM stg.ordersystem_restaurants")
                                                            
    result = cursor.fetchall()
    connection.close()
    
    temp_list = []

    for i in result:
        j = json.loads(i[0])
        temp_list.append(j)

    df = pd.DataFrame(temp_list)
    df = df.drop(columns=['menu'])
    df['active_to'] = '2099-12-31 00:00:00.000'

    print(df.columns)
    print(df)

    connection = pg_hook.get_conn()
    cursor = connection.cursor()
 
    # Запись данных в базу
    
    insert_stmt = f"INSERT INTO dds.dm_restaurants (restaurant_id, restaurant_name, active_from, active_to) VALUES (%s, %s, %s, %s)"

    cursor.executemany(insert_stmt, df.values)
    connection.commit()
    connection.close()



    return result

# Создание DAG
with DAG(
    "stg_to_dds_restaurants_dag", 
    start_date=datetime(2021, 10, 1), 
    schedule_interval=None
    ) as dag:
 
    read_data = PythonOperator(
        task_id="read_data_from_stg",
        python_callable=read_data_from_stg
    )
 
read_data 