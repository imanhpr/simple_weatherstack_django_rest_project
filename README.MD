# Django-Restful-Weatherstack-API

This is a simple Django restful project. I made this project for practice and it has a lot of bugs. In this project, I using Redis as a cache for my Django API.

---
### if you want to run it in your system you need to do the following steps:

 1. First of all, you need to install [**Pipenv**](https://pipenv-es.readthedocs.io/es/stable/) to make an isolated environment for python and django.
 2. Go to your favorite command line and enter this command ```pipenv sync```.
 3. then ```pipenv shell```.
 4. Linux :```python3 manage.py migrate``` Windows: ```python manage.py migrate ```.
 5. Then export your weatherstack.com API key in the environment variables ```export WEATHERSTACK_API_KEY=your_api_key_here```.
 6. create superuser for Django admin with the following command ```python3 mange.py createsuperuser```.
 7. Enter ```python3 manage.py shell``` then run the commands below :
```python
>>> import json
>>> from pathlib import Path
>>> from api.models import City
>>> city_file = Path('api','city.json')
>>> dummy_data = [City(name=city_name) for city_name in json.load(city_file.open()).values()]
>>> City.objects.bulk_create(dummy_data)
>>> exit()
```
 8. Now you can run django with ```python3 manage.py runserver``` .
---
#### API End Points :
 
|End Point| Description |
|--|--|
|/city | return list of all city |
|/city/**{id}** | return detial of selected city |
|city/weather/**{id}** | current weather of the selected city