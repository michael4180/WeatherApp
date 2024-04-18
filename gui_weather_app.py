from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
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
    if not response.ok:
        return None
    return response.json()


class WeatherApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.city_name_input = TextInput(hint_text='Enter a city name', size_hint_y=None, height=30)
        self.layout.add_widget(self.city_name_input)

        self.get_weather_button = Button(text='Get Weather', size_hint_y=None, height=30)
        self.get_weather_button.bind(on_press=self.display_weather)
        self.layout.add_widget(self.get_weather_button)

        self.result_label = Label(size_hint_y=None)
        self.layout.add_widget(self.result_label)

        return self.layout

    def display_weather(self, instance):
        city_name = self.city_name_input.text
        weather_data = get_weather(city_name)
        if weather_data and weather_data.get("cod") == 200:
            forecast_data = get_weather(city_name, forecast=True)
            weather_text = f"Weather in {weather_data['name']}: {weather_data['weather'][0]['description']}\n"
            weather_text += f"Temperature: {weather_data['main']['temp']}°C, Humidity: {weather_data['main']['humidity']}%\n"
            weather_text += "\n5-Day Weather Forecast:\n"
            for item in forecast_data['list']:
                time = item['dt_txt']
                temp = item['main']['temp']
                description = item['weather'][0]['description']
                weather_text += f"{time}: {description}, Temp: {temp}°C\n"
            self.result_label.text = weather_text
        else:
            self.result_label.text = "Failed to retrieve weather data."


if __name__ == '__main__':
    WeatherApp().run()