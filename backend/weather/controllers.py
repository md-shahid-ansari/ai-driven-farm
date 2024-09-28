import requests
import os
from dotenv import load_dotenv
load_dotenv()

WEATHER_MAP_API_KEY = os.getenv('WEATHER_MAP_API_KEY', '')
WEATHER_MAP_URL = os.getenv('WEATHER_MAP_URL', 'http://api.openweathermap.org/data/2.5')

def get_weather(lat, lon):
    weather_url = f'{WEATHER_MAP_URL}/weather?lat={lat}&lon={lon}&appid={WEATHER_MAP_API_KEY}&units=metric'
    response = requests.get(weather_url)
    return response.json()