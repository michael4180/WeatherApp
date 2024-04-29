from flask import Flask, render_template, request, send_file
from config import openweather_api_key as api_key
import requests
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

def get_weather(city_name, forecast=False):
    if not forecast:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
    else:
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None
    return response.json()

def plot_forecast(forecast):
    if forecast:
        times = [item['dt_txt'] for item in forecast['list']]
        temps = [item['main']['temp'] for item in forecast['list']]

        plt.figure(figsize=(10, 5))
        plt.plot(times, temps, marker='o', linestyle='-', color='b')
        plt.title('5 Day Forecast')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches="tight")
        img.seek(0)
        plt.close()
        return img

@app.route('/forecast.png')
def forecast_img():
    city_name = request.args.get('city')
    forecast = get_weather(city_name, forecast=True)
    img = plot_forecast(forecast)
    return send_file(img, mimetype='image/png')

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

