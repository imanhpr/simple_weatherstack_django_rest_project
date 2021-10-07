from datetime import timedelta

from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from icecream import ic

from .models import City, Weather
from .serializers import CitySerializer, WeatherSerializer
from .weatherstackapi import clean_current_weather

from django.core.cache import cache


@api_view(['GET'])
def city_list(request, format=None):
    '''

    '''
    if request.method == 'GET':
        city_objects_list = cache_or_db(City.objects.all, 'city_objects_list')
        serializer = CitySerializer(city_objects_list, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def city_detail(request, pk, format=None):
    # TODO: it can be cleaner #1
    if request.method == 'GET':
        try:
            city = cache_or_db(
                City.objects.get, key_name=f'city-id-{pk}', pk=pk)
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CitySerializer(city)
        return Response(serializer.data)


@api_view(['GET'])
def city_weather_detail(request, pk, format=None):
    # TODO: it can be cleaner #1

    # Get City Name From Db or cache
    if request.method == 'GET':
        try:
            city = cache_or_db(
                City.objects.get, key_name=f'city-id-{pk}', pk=pk)
            weather = cache_or_db(
                Weather.objects.get, key_name=f'city-weather-id-{pk}', new_timeout=False, city=city,
            )
        except City.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Weather.DoesNotExist:
            ic('weather dose not exist')
            get_weather = clean_current_weather(city.name)
            new_Weather_obj = Weather.objects.create(
                city=city,  # Foreign Key For Relationship
                **get_weather
            )
            cache.set(f'city-weather-id-{pk}', new_Weather_obj)
            ic('new weather add to redis and db')
            serializer = WeatherSerializer(new_Weather_obj)
            return Response(serializer.data)

        if timezone.now() > weather.time + timedelta(hours=1, seconds=0):
            ic('weather 1 houre time is expire')
            get_weather = clean_current_weather(city.name)
            new_Weather_obj = Weather.objects.create(
                city=city,  # Foreign Key For Relationship
                **get_weather
            )
            cache.set(f'city-weather-id-{pk}', new_Weather_obj)
            ic('new weather add to database for 1 houre time expire')
            serializer = WeatherSerializer(new_Weather_obj)
            return Response(serializer.data)
        ic('good weather exsit in db or cache and return it')
        t = abs(timezone.now() - (weather.time + timedelta(hours=1, seconds=0)))
        ic(f'{t} for make new request to weatherapistack')
        serializer = WeatherSerializer(weather)
        return Response(serializer.data)

    # Weahter of city


def cache_or_db(query: callable, key_name: str, new_timeout=True, **kwargs):
    data = cache.get(key_name)
    if not data:
        data = query(**kwargs)
        cache.set(key_name, data)
        ic('Data From DataBase')
        return data
    if new_timeout:
        cache.expire(key_name, timeout=5 * 60)
    ic(f'Data From redis | TTL:{cache.ttl(key_name)}')
    return data
