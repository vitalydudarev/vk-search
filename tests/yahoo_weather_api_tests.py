from yahoo_api import YahooWeatherApi
from client import HttpClient

client = HttpClient(timeout=10)
api = YahooWeatherApi(client)

print api.get_forecast(834463)
