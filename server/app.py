from flask import Flask, render_template

from .routes.error_routes import error_routes
from .routes.spotify_routes import spotify_routes
from .routes.smartlights_routes import smartlight_routes
from .routes.computer_routes import computer_routes
from .routes.discord_routes import discord_routes

import requests
import json

app = Flask(__name__)

app.register_blueprint(error_routes)
app.register_blueprint(spotify_routes)
app.register_blueprint(smartlight_routes)
app.register_blueprint(computer_routes)
app.register_blueprint(discord_routes)


def get_weather_data():
    try:
        with open("./config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        weather_config = config["weather"]
        api = f"http://api.weatherapi.com/v1/current.json?key={weather_config['api_key']}&q=CT4&aqi=no"
        response = requests.get(api)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data['current']['temp_c'],
                "condition": data['current']['condition']['text'],
                "location": data['location']['name']
            }
    except Exception as e:
        print(f"Weather API error: {e}")
    return None

@app.route("/home/update_weather_temp")
def update_weather_temp():
    data = get_weather_data()
    if data:
        return f'''
        <p class="text-neutral-500 font-semibold text-[12px]">Temperature</p>
        <h1 class="text-white font-semibold text-[29px]">{data["temp"]}°C</h1>
        '''
    else:
        return '<p class="text-red-500">Error loading temperature</p>'

@app.route("/home/update_weather_condition")
def update_weather_condition():
    data = get_weather_data()
    if data:
        return f'''
        <p class="text-neutral-500 font-semibold text-[12px]">Condition</p>
        <h1 class="text-white font-semibold text-[29px]">{data["condition"]}</h1>
        '''
    else:
        return '<p class="text-red-500">Error loading condition</p>'

@app.route("/home/update_weather_location")
def update_weather_location():
    data = get_weather_data()
    if data:
        return f'''
        <p class="text-neutral-500 font-semibold text-[12px]">Location</p>
        <h1 class="text-white font-semibold text-[29px]">{data["location"]}</h1>
        '''
    else:
        return '<p class="text-red-500">Error loading location</p>'

@app.route("/")
def index():
    return render_template("home.html")

def run_flask():
    app.run(host="0.0.0.0", port=5420, debug=False, use_reloader=False)
