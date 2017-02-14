from wrappers import YahooWeatherWrapper, NbrbRatesWrapper
from storage import Storage
import datetime


class ServicesFacade:
    def __init__(self, storage, client):
        print 'Initializing services'
        self.__storage = storage
        self.__rates_wrapper = NbrbRatesWrapper(client)
        self.__weather_wrapper = YahooWeatherWrapper(client)
        weather = self.__weather_wrapper.get_forecast(834463)
        cur_rate = self.__rates_wrapper.get_rate('USD', datetime.date.today())
        storage.add('weather', weather)
        storage.add('cur_rate', cur_rate)
        print 'Initialized services'

    def weather(self):
        return self.__weather_wrapper

    def rates(self):
        return self.__rates_wrapper