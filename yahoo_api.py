import urllib2
import json
from api import ApiResponse


class YahooWeatherApi:
    URI = 'https://query.yahooapis.com/v1/public/yql?q={query}&format=json&diagnostics=true&callback='
    QUERY = 'select item from weather.forecast where woeid = {location_id} and u=\'c\''

    def __init__(self, client):
        self.__client = client

    def get_forecast(self, location_id):
        query = self.QUERY.replace('{location_id}', str(location_id))
        query = urllib2.quote(query)
        uri = self.URI.replace('{query}', query)

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error').to_json()

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
            return ApiResponse(has_error=True, error_description='Yahoo API error').to_json()

        res['condition'] = res_condition
        res['forecast'] = res_forecast

        return ApiResponse(result=res).to_json()
