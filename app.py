import vk_api
import config
from flask import Flask, render_template, request
from yahoo_api import YahooWeatherApi

app = Flask(__name__)
config = config.load_config('config.json')
api = vk_api.VkApi(config.access_token, config.proxy)
weather_api = YahooWeatherApi()

@app.route("/")
def hello():
    return render_template("search.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    if request.method == 'POST':
        query = request.form['value']
        return api.search(query)

@app.route("/audios", methods=['POST', 'GET'])
def audios():
    if request.method == 'GET':
        return render_template("audios.html")
    if request.method == 'POST':
        return api.get(config.user_id)

@app.route("/weather")
def weather():
    return weather_api.get_forecast(834463)

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)