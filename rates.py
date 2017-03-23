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
    url_range = "http://www.nbrb.by/API/ExRates/Rates/Dynamics/{ccy_id}?startDate={from}&endDate={to}"

    def __init__(self, client):
        self.init_failed = False
        self.__client = client
        self.__cur_mapping = self.get_currencies()
        if len(self.__cur_mapping) == 0:
            self.init_failed = True
            logging.debug(u'Initialization failed')

    def get_rate(self, currency, date):
        return self.get_rates(currency, date, date)

    def get_rates(self, currency, from_date, to_date):
        if self.init_failed is True:
            return ApiResponse(has_error=True, error_description='Connection error on initialization').to_json()

        if currency not in self.__cur_mapping:
            return ApiResponse(has_error=True, error_description='Unsupported/unknown currency').to_json()

        currency_id = self.__cur_mapping[currency]

        uri = self.url_range \
            .replace("{ccy_id}", str(currency_id)) \
            .replace("{from}", utils.date_to_string(from_date, self.DATE_FORMAT)) \
            .replace("{to}", utils.date_to_string(to_date, self.DATE_FORMAT))

        response = self.__client.get_response(uri)
        if response.has_error:
            return ApiResponse(has_error=True, error_description='Connection error').to_json()

        j_resp = json.loads(response.response_text)

        rates = {}

        for item in j_resp:
            date = utils.string_to_date(item['Date'], self.ISO_DATE_FORMAT)
            str_date = utils.date_to_string(date, self.DATE_FORMAT)
            rate = item['Cur_OfficialRate']
            rates[str_date] = rate

        return ApiResponse(result=collections.OrderedDict(sorted(rates.items()))).to_json()

    def get_currencies(self):
        response = self.__client.get_response(self.url_currencies)
        if response.has_error:
            return []
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
