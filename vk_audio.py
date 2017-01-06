import requests
import json
import urllib
import re

class VkAudio:
    def __init__(self):
        self.__url = 'https://vk.com/al_audio.php'
        self.__cookie = ''

    def get_audio_info(self, audio_id):
        headers = {"cookie": self.__cookie}
        params = {"act": "reload_audio", "al": 1, "ids": audio_id}
        encoded_params = urllib.urlencode(params)

        resp = requests.post(self.__url, data=encoded_params, headers=headers)

        match = re.search('<!json>(.*)<!><!bool>', resp.content)
        j_str = match.group(1)

        return json.loads(j_str)

    def get_audio_list(self, owner_id):
        headers = {"cookie": self.__cookie}
        params = {"act": "load_silent", "al": 1, "album_id": -2, "band": False, "owner_id": owner_id}
        encoded_params = urllib.urlencode(params)

        resp = requests.post(self.__url, data=encoded_params, headers=headers)

        match = re.search('<!json>(.*)<!><!pageview_candidate>', resp.content)
        j_str = unicode(match.group(1), 'cp1251')

        j_object = json.loads(j_str)
        return j_object['list']