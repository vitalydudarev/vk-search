import requests
import json
import urllib
import re
from HTMLParser import HTMLParser

class VkAudio:
    # the constructor takes cookie parameter in the format 'remixsid={id}'
    def __init__(self, cookie):
        self.__url = 'https://vk.com/al_audio.php'
        self.__cookie = cookie
        self.__parser = HTMLParser()

    # returns an array of Audio objects
    def get_audio_info(self, audio_ids):
        ids = ','.join(str(x) for x in audio_ids)
        headers = {"cookie": self.__cookie}
        params = {"act": "reload_audio", "al": 1, "ids": ids}

        audio_info = self.__get_response(headers, params)
        result = []

        for item in audio_info:
            track_id = item[1] + "_" + item[0]
            link = item[2]
            result.append({"track_id": track_id, "link": link})

        if len(result) == 1:
            return json.dumps(result[0])
        else:
            return json.dumps(audio_info)

    def get_audio_list(self, owner_id):
        headers = {"cookie": self.__cookie}
        params = {"act": "load_silent", "al": 1, "album_id": -2, "band": False, "owner_id": owner_id}

        j_object = self.__get_response(headers, params)
        audio_list = j_object['list']

        result = []

        for item in audio_list:
            track_id = item[1] + "_" + item[0]
            title = self.__parser.unescape(item[4] + " - " + item[3])
            result.append({"track_id": track_id, "title": title})

        return json.dumps(result)

    def __get_response(self, headers, params):
        encoded_params = urllib.urlencode(params)

        resp = requests.post(self.__url, data=encoded_params, headers=headers)

        match = re.search('<!json>(.*)<!>', resp.content)
        j_str = unicode(match.group(1), 'cp1251')

        return json.loads(j_str)