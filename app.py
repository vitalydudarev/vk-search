from flask import Flask, render_template, request
import config
from facade import Facade

app = Flask(__name__)
config = config.load_config('config.json')
facade = Facade(config)


@app.route("/")
def home():
    rate = facade.get_current_rate()
    return render_template("home.html", cur_rate=rate)


@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    if request.method == 'POST':
        query = request.form['value']
        return facade.vk_search(query)


@app.route("/audios", methods=['POST', 'GET'])
def audios():
    if request.method == 'GET':
        return render_template("audios.html")
    if request.method == 'POST':
        return facade.vk_get_audio_list(config.user_id)


@app.route("/rates")
def rates():
    return render_template("rates.html")


@app.route("/get_rates")
def get_rates():
    currency = request.args.get('currency')
    tenor = request.args.get('tenor')
    return facade.get_rates(currency, tenor)


@app.route("/audio_info/<id>")
def audio_info(id):
    return facade.vk_get_audio_info([id])


@app.route("/weather")
def weather():
    return facade.get_current_weather()


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True)
