import urllib2
import json
from api import ApiResponse


class YahooGeoApi:
    URI = 'https://query.yahooapis.com/v1/public/yql?q={query}&format=json&diagnostics=true&callback='
    QUERY_PLACE = 'select * from geo.places(1) where text = "{query}"'
    QUERY_PLACES = 'select * from geo.places where text = "{query}"'

    def __init__(self, client):
        self.__client = client

    def get_place(self, query):
        return self.__get_place_internal(query, self.QUERY_PLACE)

    def get_places(self, query):
        return self.__get_place_internal(query, self.QUERY_PLACES)

    def __get_place_internal(self, query, yql_query):
        query = yql_query.replace('{query}', query)
        query = urllib2.quote(query)
        uri = self.URI.replace('{query}', query)

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error')

        j_resp = json.loads(response.response_text)
        
        if j_resp['query']['results'] is None:
            return ApiResponse(result=[])

        places = j_resp['query']['results']['place']
        count = int(j_resp['query']['count'])
        if count == 1:
            places = [places]

        results = []

        for place in places:
            woeid = place['woeid']
            name = place['name']
            place_type = place['placeTypeName']['content']
            country = place['country']['content']

            res = {'name': name, 'woeid': woeid, 'placeType': place_type, 'country': country}
            results.append(res)

        return ApiResponse(result=results)


class YahooWeatherApi:
    URI = 'https://query.yahooapis.com/v1/public/yql?q={query}&format=json&diagnostics=true&callback='
    QUERY = 'select item from weather.forecast where woeid = {location_id}'

    def __init__(self, client, use_celcius=True):
        self.__client = client
        if use_celcius:
            self.QUERY += ' and u=\'c\''

    def get_forecast(self, location_id):
        query = self.QUERY.replace('{location_id}', str(location_id))
        query = urllib2.quote(query)
        uri = self.URI.replace('{query}', query)

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error')

        j_resp = json.loads(response.response_text)

        res = {}
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
            return ApiResponse(has_error=True, error_description='Yahoo API error')

        res['condition'] = res_condition
        res['forecast'] = res_forecast

        return ApiResponse(result=res)
