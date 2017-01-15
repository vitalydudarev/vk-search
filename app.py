import config
import datetime
import utils
from vk_api import VkApi
from flask import Flask, render_template, request
from wrappers import YahooWeatherWrapper, NbrbRatesWrapper
from storage import Storage
from vk_audio import VkAudio
from rates import NbrbRates

app = Flask(__name__)
config = config.load_config('config.json')
api = VkApi(config.access_token, config.proxy)
vk_audio = VkAudio("", config.proxy)
wrapper = YahooWeatherWrapper(config.proxy)
storage = Storage()
nbrb_rates = NbrbRatesWrapper()

@app.route("/")
def home():
    return render_template("home.html")

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
        return vk_audio.get_audio_list(config.user_id)

@app.route("/rates")
def rates():
    return render_template("rates.html")

@app.route("/get_r")
def test():
    currency = request.args.get('currency')
    s_start = request.args.get('start')
    s_end = request.args.get('end')
    start = utils.string_to_date(s_start, "%Y-%m-%d")
    end = utils.string_to_date(s_end, "%Y-%m-%d")
    return nbrb_rates.get_rates(currency, start, end)

@app.route("/get_rates/<ccy_id>")
def get_rates(ccy_id):
    return nbrb_rates.get_rates(ccy_id, datetime.date(2016, 12, 1), datetime.date(2017, 01, 14))

@app.route("/audio_info/<id>")
def audio_info(id):
    return vk_audio.get_audio_info([id])

@app.route("/weather")
def weather():
    weather = storage.get('weather')
    if weather is None:
        weather = wrapper.get_forecast(834463)
        storage.add('weather', weather)
    return weather

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)