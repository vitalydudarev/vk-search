import json
import re
from HTMLParser import HTMLParser
from api import ApiResponse


class VkAudio:
    # the constructor takes cookie parameter in the format 'remixsid={id}'
    def __init__(self, cookie, client):
        self.__url = 'https://vk.com/al_audio.php'
        self.__cookie = cookie
        self.__client = client
        self.__parser = HTMLParser()

    def get_audio_info(self, audio_ids):
        ids = ','.join(str(x) for x in audio_ids)
        headers = {'cookie': self.__cookie}
        params = {'act': 'reload_audio',
                  'al': 1, 'ids': ids}

        items = self.__get_response(headers, params)
        if items is None:
            return ApiResponse(has_error=True, error_description='Cookie has expired.')

        result = []

        for item in items:
            track_id = str(item[1]) + '_' + str(item[0])
            link = item[2]
            result.append({'track_id': track_id, 'link': link})

        res = result[0] if len(result) == 1 else result

        return ApiResponse(result=res)

    # returns a playlist of the size of 100 records
    def get_playlist(self, owner_id, offset=0):
        headers = {'cookie': self.__cookie}
        params = {'act': 'load_section',
                  'al': 1,
                  'claim': 0,
                  'offset': offset,
                  'owner_id': owner_id,
                  'playlist_id': -1,
                  'type': 'playlist'}

        return self.__handle(headers, params)

    def search(self, query, offset=0):
        headers = {'cookie': self.__cookie}
        params = {'act': 'load_section',
                  'al': 1,
                  'claim': 0,
                  'offset': offset,
                  'search_history': 0,
                  'search_q': query,
                  'type': 'search'}

        return self.__handle(headers, params)

    def __handle(self, headers, params):
        resp_internal = self.__get_response(headers, params)
        if resp_internal is None:
            return ApiResponse(has_error=True, error_description='Cookie has expired.')

        items = resp_internal['list']
        result = []

        for item in items:
            track_id = str(item[1]) + '_' + str(item[0])
            title = self.__parser.unescape(item[4] + " - " + item[3])
            duration = item[5]
            result.append({'track_id': track_id, 'title': title, 'duration': duration})

        response = {'hasMore': True if resp_internal['hasMore'] == 1 else False,
                    'nextOffset': resp_internal['nextOffset'],
                    'totalCount': resp_internal['totalCount'],
                    'items': result}

        return ApiResponse(result=response)

    def __get_response(self, headers, params):
        resp = self.__client.post(self.__url, headers, params)

        match = re.search('<!json>(.*?)(<!>)', resp.content)
        if match is None:
            return None

        j_str = match.group(1).decode('cp1251').encode('utf8')

        return json.loads(j_str)
