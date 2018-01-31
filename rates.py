import json
import datetime
import collections
import logging
import utils
from api import ApiResponse


class Currency:
    def __init__(self, id, abbreviation):
        self.id = id
        self.abbreviation = abbreviation


class NbrbRates:
    DATE_FORMAT = "%Y-%m-%d"
    ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

    url_currencies = "http://www.nbrb.by/API/ExRates/Currencies"
    url_dynamics = "http://www.nbrb.by/API/ExRates/Rates/Dynamics/{ccy_id}?startDate={from}&endDate={to}"
    url_today_rate = "http://www.nbrb.by/API/ExRates/Rates/{ccy_id}?ParamMode=2"
    url_rate = "http://www.nbrb.by/API/ExRates/Rates/Usd?onDate={date}&ParamMode=2"

    def __init__(self, client):
        self.__client = client
        self.__cur_mapping = None

    def get_today_rate(self, currency):
        uri = self.url_today_rate.replace('{ccy_id}', currency)

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error')

        j_resp = json.loads(response.response_text)
        return ApiResponse(result=j_resp['Cur_OfficialRate'])

    def get_rate(self, currency, date):
        uri = self.url_rate.replace('{ccy_id}', currency).replace('{date}', utils.date_to_string(date, self.DATE_FORMAT))

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error')

        j_resp = json.loads(response.response_text)
        return ApiResponse(result=j_resp['Cur_OfficialRate'])

    def get_rates_dynamics(self, currency, from_date, to_date):
        if self.__cur_mapping is None:
            self.__cur_mapping = self.get_currencies()
            if self.__cur_mapping is None or len(self.__cur_mapping) == 0:
                logging.debug(u'Initialization failed')
                return ApiResponse(has_error=True, error_description='Connection error on initialization')

        if currency not in self.__cur_mapping:
            return ApiResponse(has_error=True, error_description='Unsupported/unknown currency')

        currency_id = self.__cur_mapping[currency]

        uri = self.url_dynamics \
            .replace("{ccy_id}", str(currency_id)) \
            .replace("{from}", utils.date_to_string(from_date, self.DATE_FORMAT)) \
            .replace("{to}", utils.date_to_string(to_date, self.DATE_FORMAT))

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error')

        j_resp = json.loads(response.response_text)

        rates = {}

        for item in j_resp:
            date = utils.string_to_date(item['Date'], self.ISO_DATE_FORMAT)
            str_date = utils.date_to_string(date, self.DATE_FORMAT)
            rate = item['Cur_OfficialRate']
            rates[str_date] = rate

        return ApiResponse(result=collections.OrderedDict(sorted(rates.items())))

    def get_currencies(self):
        response = self.__client.get_response(self.url_currencies)
        if response.has_error:
            return None
        else:
            response_text = json.loads(response.response_text)
            cur_mapping = {}

            for cur in response_text:
                cur_mapping[cur['Cur_Abbreviation']] = cur['Cur_ID']

            return cur_mapping

    def __date_to_string(self, date):
        return date.strftime(self.DATE_FORMAT)

    def __string_to_date(self, str, format=None):
        if format is None:
            format = self.DATE_FORMAT
        return datetime.datetime.strptime(str, format)
