from django.urls import path
from .views import city_list , city_detail , city_weather_detail
urlpatterns = [
    path('city/',city_list),
    path('city/<int:pk>',city_detail),
    path('city/weather/<int:pk>',city_weather_detail),
]

