import requests
from config import openweather_api_key as api_key

def get_weather(city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

def display_weather(weather_data):
    if weather_data.get("cod") != 200:
        print("Failed to get the weather data:", weather_data.get("message"))
    else:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        print(f"Weather in {weather_data['name']}: {description}")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

def main():
    city_name = input("Enter a city name: ")
    weather_data = get_weather(city_name)
    display_weather(weather_data)

if __name__ == "__main__":
    main()