from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Assuming you have your openweather_api_key in a config module
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

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    if request.method == 'POST':
        city_name = request.form['city']
        weather = get_weather(city_name)
        if weather:
            forecast = get_weather(city_name, forecast=True)
    return render_template('weather.html', weather=weather, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)
