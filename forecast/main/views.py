from django.shortcuts import render
from django.views.generic.base import View
from transliterate import translit, get_available_language_codes
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy.geocoders import Nominatim
import re

class Main(View):
    def get(self, request):
        return render(request, "main/main.html")
    def post(self, request):
        try:
            if request.method == 'POST': 
                city = request.POST['city'] 
                if re.match("^[A-Za-zА-Яа-я]*$", city):
                    geolocator = Nominatim(user_agent="Tester")
                    adress = city
                    location = geolocator.geocode(adress)
                else:
                    return render(request, "main/main.html", context={'error': 'Не удалось найти такой город'}) 

        
            # Setup the Open-Meteo API client with cache and retry on error
            cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
            retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
            openmeteo = openmeteo_requests.Client(session = retry_session)

            # Make sure all required weather variables are listed here
            # The order of variables in hourly or daily is important to assign them correctly below
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "hourly": ["temperature_2m", "weather_code"]
            }
            responses = openmeteo.weather_api(url, params=params)

            # Process first location. Add a for-loop for multiple locations or weather models
            response = responses[0]


            # Process hourly data. The order of variables needs to be the same as requested.
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
            hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
            
            if int(hourly_weather_code[12]) == 0:
                weather_code_img = 'img/Sun.jpg'
                weather_code_name = 'Ясно'
            elif int(hourly_weather_code[12]) in {1, 2, 3}:
                weather_code_img = 'img/Cloud.jpg'
                weather_code_name = 'Облачно'
            elif int(hourly_weather_code[12]) in {45, 48, 51, 53, 55, 56, 57}:
                weather_code_img = 'img/Drizzle.jpg'
                weather_code_name = 'Морось'
            elif int(hourly_weather_code[12]) in {61, 63, 65, 66, 67}:
                weather_code_img = 'img/Rain.jpg'
                weather_code_name = 'Дождь'
            elif int(hourly_weather_code[12]) in {71, 73, 75, 77, 85, 86}:
                weather_code_img = 'img/Snow.jpg'
                weather_code_name = 'Снег'
            elif int(hourly_weather_code[12]) in {80, 81, 82, 95, 96, 99}:
                weather_code_img = 'img/Rainfall.jpg'
                weather_code_name = 'Гроза'

            context = {
                'city': city,
                'temperature_one': int(hourly_temperature_2m[0]),
                'temperature_two': int(hourly_temperature_2m[12]),
                'weather_code': weather_code_img,
                'weather_code_name': weather_code_name
            }
            return render(request, "main/main.html", context=context) 
        except:
            return render(request, "main/main.html", context={'error': 'Не удалось найти такой город'}) 
    
