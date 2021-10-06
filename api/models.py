from django.db import models


class City(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name

class Weather(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.CASCADE ,related_name='weathers'
    )
    time = models.DateTimeField(auto_now_add=True)
    is_day = models.BooleanField()

    weather_descriptions = models.CharField(max_length=60)
    wind_dir = models.CharField(max_length=60)

    feelslike = models.IntegerField()
    humidity = models.IntegerField()
    cloudcover = models.IntegerField()
    pressure = models.IntegerField()
    temperature = models.IntegerField()
    weather_code = models.IntegerField()
    wind_degree = models.IntegerField()
    wind_speed = models.IntegerField()

    class Meta :
        ordering = ['-pk']

    def __str__(self) -> str:
        return f'{self.city.name} | temp:{self.temperature}'