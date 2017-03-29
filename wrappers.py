from yahoo_api import YahooWeatherApi
from rates import NbrbRates
import json


# this wrapper is used to correctly load weather forecast
# because sometimes Yahoo API returns an error without data
class YahooWeatherWrapper:
    def __init__(self, client):
        self.__api = YahooWeatherApi(client)
        self.__retry_count = 10

    def get_forecast(self, location_id):
        forecast = None

        for i in range(0, self.__retry_count):
            forecast = self.__api.get_forecast(location_id)
            j_forecast = json.loads(forecast)
            if j_forecast['has_error'] is False:
                break

        return forecast


class NbrbRatesWrapper:
    def __init__(self, client):
        self.__retry_count = 10
        self.__api = NbrbRates(client)

    def get_today_rate(self, currency):
        rates = None

        for i in range(0, self.__retry_count):
            rates = self.__api.get_today_rate(currency)
            j_rates = json.loads(rates)
            if j_rates['has_error'] is False:
                return rates

        return rates

    def get_rate(self, currency, date):
        rates = None

        for i in range(0, self.__retry_count):
            rates = self.__api.get_rate(currency, date)
            j_rates = json.loads(rates)
            if j_rates['has_error'] is False:
                return rates

        return rates

    def get_rates_dynamics(self, currency, from_date, to_date):
        rates = None

        for i in range(0, self.__retry_count):
            rates = self.__api.get_rates_dynamics(currency, from_date, to_date)
            j_rates = json.loads(rates)
            if j_rates['has_error'] is False:
                return rates

        return rates
