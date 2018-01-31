import datetime
import json
import logging
import re
import utils
from client import HttpClient
from scheduler import Scheduler
from storage import Storage
from vk_audio import VkAudio
from yahoo_api import YahooGeoApi, YahooWeatherApi
from rutor import RutorDataHolder
from rates import NbrbRates

logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s;%(levelname)s;%(message)s")


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class VkAudioFacade:
    def __init__(self, config):
        self.__client = HttpClient(config.proxy, 10)
        self.__vk_audio = VkAudio(config.vk_cookie, self.__client)

    def audio_search(self, query, offset=0):
        return self.__vk_audio.search(query, offset).to_json()

    def get_audio_list(self, user_id, offset=0):
        return self.__vk_audio.get_playlist(user_id, offset).to_json()

    def get_audio_info(self, id):
        return self.__vk_audio.get_audio_info(id).to_json()

class WeatherFacade:
    def __init__(self, config):
        self.__storage = Storage()
        self.__client = HttpClient(config.proxy, 10)
        self.__weather_service = YahooWeatherApi(self.__client)
        self.__update_weather()
        self.__weather_scheduler = Scheduler(self.__update_weather)
        self.__weather_scheduler.start(3600, 00)

    def get_weather_forecast(self):
        weather = self.__storage.get('weather')
        return weather

    def __update_weather(self):
        weather = self.__weather_service.get_forecast(834463).to_json()
        logging.info(u'Updated weather')
        self.__storage.add('weather', weather)

class RatesFacade:
    def __init__(self, config):
        self.__storage = Storage()
        self.__client = HttpClient(config.proxy, 10)
        self.__rates_service = NbrbRates(self.__client)
        self.__update_rates()
        self.__rates_scheduler = Scheduler(self.__update_rates)
        self.__rates_scheduler.start(3600 * 24, 00, 00)

    def get_rate(self):
        cur_rate = self.__storage.get('cur_rate')
        res = json.loads(cur_rate)
        return res['result']

    def get_rates(self, currency, tenor, start=None, end=None):
        if tenor is not None:
            match = re.search('(\\d+)([mMwW])', tenor)
            if match is not None:
                tenor_i = int(match.group(1))
                m_w = match.group(2)
                key = 'rates-' + str(datetime.date.today()) + str(tenor_i) + m_w
                res = self.__storage.get(key)
                if res is None:
                    end = datetime.date.today()
                    start = None
                    if m_w in ['m', 'M']:
                        start = utils.month_delta(end, tenor_i * -1)
                    elif m_w in ['w', 'W']:
                        start = end - datetime.timedelta(days=7 * tenor_i)
                    rates = self.__rates_service.get_rates_dynamics(currency, start, end).to_json()
                    self.__storage.add(key, rates)
                    return rates
                else:
                    return res
        else:
            s_start = utils.string_to_date(start, "%Y-%m-%d")
            s_end = utils.string_to_date(end, "%Y-%m-%d")
            return self.__rates_service.get_rates_dynamics(currency, s_start, s_end).to_json()

    def __update_rates(self):
        cur_rate = self.__rates_service.get_today_rate('USD').to_json()
        logging.info(u'Updated rates')
        self.__storage.add('cur_rate', cur_rate)

class Facade:
    def __init__(self, config):
        self.__storage = Storage()
        self.__client = HttpClient(config.proxy, 10)
        self.__geo_service = YahooGeoApi(self.__client)
        self.__rutor_data_holder = RutorDataHolder('dump.txt')

    def get_date_formatted(self):
        return datetime.date.today().strftime("%A, %d %B %Y")

    def get_place_woeid(self, query):
        return self.__geo_service.get_places(query).to_json()

    def get_rutor_data(self, index=0):
        data = self.__rutor_data_holder.get_data(index)
        return data
