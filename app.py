import datetime as dt
import requests

def kelvinToCelsius(kelvin):
    celsius=kelvin-273.15
    return celsius

def weatherData(city):
    BASE_URL='http://api.openweathermap.org/data/2.5/weather?'
    API_KEY=open('apiKey.txt','r').read()
    CITY=city
    url=BASE_URL+'appid='+API_KEY+'&q='+CITY
    response=requests.get(url).json()
    temp_kel=response['main']['temp']
    temp_cel=kelvinToCelsius(temp_kel)
    feels_like_kel=response['main']['feels_like']
    feels_like_cel=kelvinToCelsius(feels_like_kel)
    humidity=response['main']['humidity']
    description=response['weather'][0]['description']
    sunrise_time=dt.datetime.utcfromtimestamp(response['sys']['sunrise']+response['timezone'])
    sunset_time=dt.datetime.utcfromtimestamp(response['sys']['sunset']+response['timezone'])
    data={'temp_celsius': temp_cel,
          'temp_kelvin':temp_kel,
          'feels_like_celsius':feels_like_cel,
          'feels_like_kelvin':feels_like_kel,
          'humidity':humidity,
          'description':description,
          'sunrise_time':sunrise_time,
          'sunset_time':sunset_time}
    return data