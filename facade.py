import re
from client import HttpClient
from vk_audio import VkAudio
from wrappers import YahooWeatherWrapper, NbrbRatesWrapper
from storage import Storage
from scheduler import Scheduler
import datetime
import json
import utils
import threading
import logging


logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s;%(levelname)s;%(message)s")


class Facade:
    def __init__(self, config):
        self.__storage = Storage()
        self.__client = HttpClient(config.proxy, 10)
        self.__vk_audio = VkAudio(config.vk_cookie, self.__client)
        self.__rates_service = NbrbRatesWrapper(self.__client)
        self.__weather_service = YahooWeatherWrapper(self.__client)
        self.__update_rates()
        self.__update_weather()
        self.__rates_scheduler = Scheduler(self.__update_rates)
        self.__weather_scheduler = Scheduler(self.__update_weather)
        self.__rates_scheduler.start(3600 * 24, 00, 00)
        self.__weather_scheduler.start(3600, 00)

    def get_current_rate(self):
        cur_rate = self.__storage.get('cur_rate')
        res = json.loads(cur_rate)
        return res['result']

    def get_current_weather(self):
        weather = self.__storage.get('weather')
        return weather

    def get_rates(self, currency, tenor, start=None, end=None):
        if tenor is not None:
            match = re.search('(\\d+)([mMwW])', tenor)
            if match is not None:
                tenor_i = int(match.group(1))
                m_w = match.group(2)
                key = 'rates-' + str(tenor_i) + m_w
                res = self.__storage.get(key)
                if res is None:
                    end = datetime.date.today()
                    start = None
                    if m_w in ['m', 'M']:
                        start = utils.month_delta(end, tenor_i * -1)
                    elif m_w in ['w', 'W']:
                        start = end - datetime.timedelta(days=7 * tenor_i)
                    rates = self.__rates_service.get_rates_dynamics(currency, start, end)
                    self.__storage.add(key, rates)
                    return rates
                else:
                    return res
        else:
            s_start = utils.string_to_date(start, "%Y-%m-%d")
            s_end = utils.string_to_date(end, "%Y-%m-%d")
            return self.__rates_service.get_rates_dynamics(currency, s_start, s_end)

    def vk_search(self, query):
        return self.__vk_audio.search(query)

    def vk_get_audio_list(self, user_id):
        return self.__vk_audio.get_audio_list(user_id)

    def vk_get_audio_info(self, id):
        return self.__vk_audio.get_audio_info(id)

    def __update_rates(self):
        cur_rate = self.__rates_service.get_today_rate('USD')
        logging.info(u'Updated rates')
        self.__storage.add('cur_rate', cur_rate)

    def __update_weather(self):
        weather = self.__weather_service.get_forecast(834463)
        logging.info(u'Updated weather')
        self.__storage.add('weather', weather)
