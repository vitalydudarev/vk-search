import urllib2
import json
from client import HttpClient


class YahooWeatherApi:
    URI = 'https://query.yahooapis.com/v1/public/yql?q={query}&format=json&diagnostics=true&callback='
    QUERY = 'select item from weather.forecast where woeid = {location_id} and u=\'c\''

    def __init__(self, proxy = {}):
        self.__client = HttpClient(proxy, 10)

    def get_forecast(self, location_id):
        query = self.QUERY.replace('{location_id}', str(location_id))
        query = urllib2.quote(query)
        uri = self.URI.replace('{query}', query)

        response = self.__client.get_response(uri)

        j_resp = json.loads(response)

        res = {}
        res_condition = {}
        res_forecast = []
        has_error = False

        results = j_resp['query']['results']

        if results is not None:
            res_item = results['channel']['item']
            condition = res_item['condition']
            forecast = res_item['forecast']
            
            res_condition = {'temp': condition['temp'], 'text': condition['text'], 'date': condition['date']}

            for item in forecast:
                res_for = {'date': item['date'], 'high': item['high'], 'low': item['low'], 'text': item['text']}
                res_forecast.append(res_for)
        else:
            has_error = True

        res['condition'] = res_condition
        res['forecast'] = res_forecast

        return {'has_error': has_error, 'result': res}