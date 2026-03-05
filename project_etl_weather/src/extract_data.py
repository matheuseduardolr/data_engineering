import requests
import json
from pathlib import Path
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

API_KEY = os.getenv('api_key')
cidade = "Maceio,BR"
url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"


def extract_weather_data(url:str) -> list:
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        logging.error("Erro de requisição.", response.content)
        return []
    
    if not data:
        logging.warning("Nenhum dado retornado.")
        return []

    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Arquivo salvo em {output_path}")
    return data