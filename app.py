import config
from vk_api import VkApi
from flask import Flask, render_template, request
from wrappers import YahooWeatherWrapper
from storage import Storage
from vk_audio import VkAudio

app = Flask(__name__)
config = config.load_config('config.json')
api = VkApi(config.access_token, config.proxy)
vk_audio = VkAudio("", config.proxy)
wrapper = YahooWeatherWrapper(config.proxy)
storage = Storage()

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