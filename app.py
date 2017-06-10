from flask import Flask, render_template, request
import config
from facade import Facade

app = Flask(__name__)
config = config.load_config('config.json')
facade = Facade(config)


@app.route("/")
def home():
    data = __get_template_data()
    return render_template("home.html", currency_rate = data['currency_rate'], forecast = data['forecast'], date_formatted=facade.get_date_formatted())


@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        data = __get_template_data()
        return render_template("search.html", currency_rate = data['currency_rate'], forecast = data['forecast'])
    if request.method == 'POST':
        query = request.form['value']
        return facade.vk_search(query)


@app.route("/audios", methods=['POST', 'GET'])
def audios():
    if request.method == 'GET':
        data = __get_template_data()
        return render_template("audios.html", currency_rate = data['currency_rate'], forecast = data['forecast'])
    if request.method == 'POST':
        return facade.vk_get_audio_list(config.user_id)


@app.route("/rates")
def rates():
    data = __get_template_data()
    return render_template("rates.html", currency_rate = data['currency_rate'], forecast = data['forecast'])


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


@app.route("/rutor")
def rutor():
    data = __get_template_data()
    return render_template("rutor.html", currency_rate=data['currency_rate'], forecast=data['forecast'])


@app.route("/get_rutor_data")
def get_rutor_data():
    index = int(request.args.get('index'))
    return facade.get_rutor_data(index)


@app.route("/search_place", methods=['POST', 'GET'])
def search_place():
    if request.method == 'GET':
        data = __get_template_data()
        return render_template("search_place.html", currency_rate = data['currency_rate'], forecast = data['forecast'])
    if request.method == 'POST':
        query = request.form['query']
        return facade.get_place_woeid(query)

def __get_template_data():
    rate = facade.get_current_rate()
    forecast = facade.get_current_weather()
    return { 'currency_rate': rate, 'forecast': forecast }

if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True)
