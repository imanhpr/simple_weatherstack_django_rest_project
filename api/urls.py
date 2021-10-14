from django.urls import path

from .views import city_detail, city_list, city_weather_detail

urlpatterns = [
    path('city/', city_list, name='city'),
    path('city/<int:pk>', city_detail, name='city-pk'),
    path('city/weather/<int:pk>', city_weather_detail, name='city-weather-pk'),
]
