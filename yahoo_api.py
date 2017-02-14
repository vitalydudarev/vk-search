import urllib2
import json
from client import HttpClient, Response


class YahooWeatherApi:
    URI = 'https://query.yahooapis.com/v1/public/yql?q={query}&format=json&diagnostics=true&callback='
    QUERY = 'select item from weather.forecast where woeid = {location_id} and u=\'c\''

    def __init__(self, client):
        self.__client = client

    def get_forecast(self, location_id):
        query = self.QUERY.replace('{location_id}', str(location_id))
        query = urllib2.quote(query)
        uri = self.URI.replace('{query}', query)

        api_response = {'has_error': False, 'result': None}

        response = self.__client.get_response(uri)
        if response.has_error:
            api_response['has_error'] = True
            api_response['error_description'] = "Connection error"
            return json.dumps(api_response)

        j_resp = json.loads(response.response_text)

        res = {}
        res_condition = {}
        res_forecast = []

        results = j_resp['query']['results']

        if results is not None:
            res_item = results['channel']['item']
            condition = res_item['condition']
            forecast = res_item['forecast']
            
            res_condition = {'temp': condition['temp'], 'text': condition['text'], 'date': condition['date']}

            for item in forecast:
                res_for = {'day': item['day'], 'date': item['date'], 'high': item['high'], 'low': item['low'], 'text': item['text']}
                res_forecast.append(res_for)
        else:
            api_response['has_error'] = True
            api_response['error_description'] = "Yahoo API error"

        res['condition'] = res_condition
        res['forecast'] = res_forecast
        
        api_response['result'] = res

        return json.dumps(api_response)