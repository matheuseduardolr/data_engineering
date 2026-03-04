from src.extract_data import extract_weather_data as extract
from src.transform_data import data_transformation as transform
from src.load_data import load_data as load

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('api_key')
# cidade = "Maceio,BR"
# url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
url = f'http://api.openweathermap.org/data/2.5/weather?q=Maceio,BR&appid={API_KEY}&units=metric&lang=pt_br'
table_name = 'maceio_weather'

def pipeline():
    try:
        logging.info(f"-> -- Etapa 1: EXTRACT --\n")
        extract(url)

        logging.info(f"-> -- Etapa 2: TRANSFORM --\n")
        df = transform()

        logging.info(f"-> -- Etapa 3: LOAD --\n")
        load(table_name, df)

        print('='*30)
        print('Pipeline concluído com sucesso!')
        print('='*30)


    except Exception as e:
        logging.error(f"-> -- Erro no pipeline: {e} --\n")
        import traceback
        traceback.print_exc()

pipeline()





