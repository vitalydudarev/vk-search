from flask import Flask, render_template, request, make_response
from jinja2 import Template
from facade import Facade, VkAudioFacade, WeatherFacade, RatesFacade
import config


app = Flask(__name__)
config = config.load_config('config.json')
facade = Facade(config)
vk_audio_facade = VkAudioFacade(config)
weather_facade = WeatherFacade(config)
rates_facade = RatesFacade(config)


@app.route("/")
def home():
    data = __get_template_data()
    return render_template("home.html", currency_rate=data['currency_rate'], forecast=data['forecast'], date_formatted=facade.get_date_formatted())


@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        data = __get_template_data()
        resp = make_response(render_template("search.html", currency_rate=data['currency_rate'], forecast=data['forecast']))
        if config.user_id is not None:
            resp.set_cookie('vkUserId', str(config.user_id))
        return resp
    if request.method == 'POST':
        query = request.form['query']
        offset = request.form['offset']
        return vk_audio_facade.audio_search(query, offset)


@app.route("/audios", methods=['POST', 'GET'])
def audios():
    if request.method == 'GET':
        data = __get_template_data()
        resp = make_response(render_template("audios.html", currency_rate=data['currency_rate'], forecast=data['forecast']))
        if config.user_id is not None:
            resp.set_cookie('vkUserId', str(config.user_id))
        return resp
    if request.method == 'POST':
        offset = request.form['offset']
        return vk_audio_facade.get_audio_list(config.user_id, offset)


@app.route("/rates")
def rates():
    data = __get_template_data()
    return render_template("rates.html", currency_rate = data['currency_rate'], forecast = data['forecast'])


@app.route("/get_rates")
def get_rates():
    currency = request.args.get('currency')
    tenor = request.args.get('tenor')
    return rates_facade.get_rates(currency, tenor)


@app.route("/audio_info/<id>")
def audio_info(id):
    return vk_audio_facade.get_audio_info([id])


@app.route("/rutor")
def rutor():
    data = __get_template_data()
    header = __get_header()
    template = Template(header)
    header_str = template.render(currency_rate=data['currency_rate'])
    return render_template("rutor.html", header=header_str, forecast=data['forecast'])


@app.route("/get_rutor_data")
def get_rutor_data():
    index = int(request.args.get('index'))
    return facade.get_rutor_data(index)


@app.route("/search_place", methods=['POST', 'GET'])
def search_place():
    if request.method == 'GET':
        data = __get_template_data()
        header = __get_header()
        template = Template(header)
        header_str = template.render(currency_rate=data['currency_rate'])
        return render_template("search_place.html", header=header_str, forecast=data['forecast'])
    if request.method == 'POST':
        query = request.form['query']
        return facade.get_place_woeid(query)


def __get_template_data():
    rate = rates_facade.get_rate()
    forecast = weather_facade.get_weather_forecast()
    return {'currency_rate': rate, 'forecast': forecast}


def __get_header():
    with open('templates/header.html', 'r') as f:
        return f.read()


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run(debug=True, use_reloader=False)
