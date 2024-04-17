
import requests
from config import openweather_api_key as api_key

def get_weather(city_name, forecast=False):
    base_url = "http://api.openweathermap.org/data/2.5/weather" if not forecast else "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None
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

def display_forecast(forecast_data):
    print("5-Day Weather Forecast:")
    for item in forecast_data['list']:
        time = item['dt_txt']
        temp = item['main']['temp']
        description = item['weather'][0]['description']
        print(f"{time}: {description}, Temp: {temp}°C")

def main():
    while True:
        city_name = input("Enter a city name: ")
        weather_data = get_weather(city_name)
        if weather_data:
            display_weather(weather_data)
            # Fetch and display 5-day forecast
            forecast_data = get_weather(city_name, forecast=True)
            display_forecast(forecast_data)
            break
        else:
            print("Invalid city name. Please try again.")

if __name__ == "__main__":
    main()