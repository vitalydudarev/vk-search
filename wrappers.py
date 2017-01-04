from yahoo_api import YahooWeatherApi
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
            J_forecast = json.loads(forecast)
            if J_forecast['has_error'] is False:
                return forecast

        return forecast