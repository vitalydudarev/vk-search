from yahoo_api import YahooGeoApi
from client import HttpClient

client = HttpClient(timeout=10)
api = YahooGeoApi(client)

print api.get_place('DXB').to_json()
print api.get_places('Minsk').to_json()
print api.get_places('Incorrectcity').to_json()
