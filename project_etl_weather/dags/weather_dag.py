from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import pandas as pd
import sys, os

sys.path.insert(0,'/opt/airflow/src')

from extract_data import extract_weather_data
from transform_data import data_transformation as transform_weather_data
from load_data import load_data as load_weather_data
from dotenv import load_dotenv

API_KEY = os.getenv('api_key')
url = f'http://api.openweathermap.org/data/2.5/weather?q=Maceio,BR&appid={API_KEY}&units=metric&lang=pt_br'

@dag(
    dag_id='weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Clima Maceió',
    schedule='0 */1 * * *',
    start_date=datetime(2026,3,3),
    catchup=False,
    tags=['weather', 'etl', 'airflow', 'maceio']
)

def weather_pipeline():
    
    @task
    def extract():
        extract_weather_data(url)
    
    @task
    def transform():
        df = transform_weather_data()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data('weather_data_maceio', df)

    extract() >> transform() >> load()

weather_pipeline()





