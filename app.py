import config
import datetime
import utils
import re
import json
from vk_api import VkApi
from flask import Flask, render_template, request
from storage import Storage
from vk_audio import VkAudio
from facade import ServicesFacade
from client import HttpClient
        

app = Flask(__name__)
config = config.load_config('config.json')
client = HttpClient(config.proxy, 10)
vk_api = VkApi(config.access_token, client)
vk_audio = VkAudio(config.vk_cookie, client)
storage = Storage()
services_facade = ServicesFacade(storage, client)

@app.route("/")
def home():
    cur_rate = storage.get('cur_rate')
    j = json.loads(cur_rate)
    return render_template("home.html", cur_rate=j['result'].values()[0])

@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    if request.method == 'POST':
        query = request.form['value']
        return vk_audio.search(query)

@app.route("/audios", methods=['POST', 'GET'])
def audios():
    if request.method == 'GET':
        return render_template("audios.html")
    if request.method == 'POST':
        return vk_audio.get_audio_list(config.user_id)

@app.route("/rates")
def rates():
    return render_template("rates.html")

@app.route("/get_rates")
def get_rates():
    currency = request.args.get('currency')
    tenor = request.args.get('tenor')
    if tenor is not None:
        match = re.search('(\\d+)([mMwW])', tenor)
        if match is not None:
            tenor_i = int(match.group(1))
            m_w = match.group(2)
            key = 'rates-' + str(tenor_i) + m_w
            res = storage.get(key)
            if res is None:
                end = datetime.date.today()
                start = None
                if m_w in ['m', 'M']:
                    start = utils.month_delta(end, tenor_i * -1)
                elif m_w in ['w', 'W']:
                    start = end - datetime.timedelta(days=7 * tenor_i)
                rates = services_facade.rates().get_rates(currency, start, end)
                storage.add(key, rates)
                return rates
            else:
                return res
    else:
        s_start = request.args.get('start')
        s_end = request.args.get('end')
        start = utils.string_to_date(s_start, "%Y-%m-%d")
        end = utils.string_to_date(s_end, "%Y-%m-%d")
        return services_facade.rates().get_rates(currency, start, end)

@app.route("/audio_info/<id>")
def audio_info(id):
    return vk_audio.get_audio_info([id])

@app.route("/weather")
def weather():
    weather = storage.get('weather')
    if weather is None:
        weather = services_facade.weather().get_forecast(834463)
        storage.add('weather', weather)
    return weather

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run(debug=True)