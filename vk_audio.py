import requests
import json
import urllib
import re

class VkAudio:
    def __init__(self, cookie):
        self.__url = 'https://vk.com/al_audio.php'
        self.__cookie = cookie

    def get_audio_info(self, audio_ids):
        ids = ','.join(str(x) for x in audio_ids)
        headers = {"cookie": self.__cookie}
        params = {"act": "reload_audio", "al": 1, "ids": ids}

        return self.__get_response(headers, params)

    def get_audio_list(self, owner_id):
        headers = {"cookie": self.__cookie}
        params = {"act": "load_silent", "al": 1, "album_id": -2, "band": False, "owner_id": owner_id}

        j_object = self.__get_response(headers, params)
        return j_object['list']

    def __get_response(self, headers, params):
        encoded_params = urllib.urlencode(params)

        resp = requests.post(self.__url, data=encoded_params, headers=headers)

        match = re.search('<!json>(.*)<!>', resp.content)
        j_str = unicode(match.group(1), 'cp1251')

        return json.loads(j_str)