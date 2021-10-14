'''
This module work with https://weatherstack.com/ API to return current
weather of location that we want.
'''
from collections import namedtuple

from os import getenv
import requests

API_KEY = getenv('WEATHERSTACK_API_KEY')

class IncorrectCityName(Exception):
    pass
        

CleanWeatherData = namedtuple(
    'CleanWeatherData',
    [
        'is_day',
        'weather_descriptions',
        'wind_dir',
        'feelslike',
        'humidity',
        'cloudcover',
        'pressure',
        'temperature',
        'weather_code',
        'wind_degree',
        'wind_speed',
    ]
)


def raw_current_weather(city: str,) -> requests.Response:
    """This function return current weather of selected city

    Args:
        city (str): city that we want weather

    Returns:
        requests.Response: requests.get response object
    """
    params = {
        'access_key': API_KEY,
        'query': city,
    }
    return requests.get('http://api.weatherstack.com/current', params)


def clean_current_weather(city: str,) -> dict:
    data = raw_current_weather(city).json()
    try : 
        return dict(
            is_day=True if data['current']['is_day'] == 'yes' else False,
            weather_descriptions=data['current']['weather_descriptions'][0],
            wind_dir=data['current']['wind_dir'],
            feelslike=data['current']['feelslike'],
            humidity=data['current']['humidity'],
            cloudcover=data['current']['cloudcover'],
            pressure=data['current']['pressure'],
            temperature=data['current']['temperature'],
            weather_code=data['current']['weather_code'],
            wind_degree=data['current']['wind_degree'],
            wind_speed=data['current']['wind_speed'],
        )
    except KeyError as e:
        print(data)
        print(e)
        raise IncorrectCityName('You Must Enter Correct City Name')
