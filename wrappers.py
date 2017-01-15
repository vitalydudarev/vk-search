from yahoo_api import YahooWeatherApi
from rates import NbrbRates
import json


# this wrapper is used to correctly load weather forecast
# because sometimes Yahoo API returns an error without data
class YahooWeatherWrapper:
    def __init__(self, proxy = {}):
        self.__wrapper = YahooWeatherApi(proxy)
        self.__retry_count = 10

    def get_forecast(self, location_id):
        forecast = None

        for i in range(0, self.__retry_count):
            forecast = self.__wrapper.get_forecast(location_id)
            j_forecast = json.loads(forecast)
            if j_forecast['has_error'] is False:
                return forecast

        return forecast


class NbrbRatesWrapper:
    def __init__(self, proxy = {}):
        self.__wrapper = NbrbRates()
        self.__retry_count = 10

    def get_rates(self, currency, from_date, to_date):
        rates = None

        for i in range(0, self.__retry_count):
            rates = self.__wrapper.get_rates(currency, from_date, to_date)
            j_rates = json.loads(rates)
            if j_rates['has_error'] is False:
                return rates

        return rates