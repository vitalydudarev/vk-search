import json
import re
from HTMLParser import HTMLParser

class VkAudio:
    # the constructor takes cookie parameter in the format 'remixsid={id}'
    def __init__(self, cookie, client):
        self.__url = 'https://vk.com/al_audio.php'
        self.__cookie = cookie
        self.__client = client
        self.__parser = HTMLParser()

    def get_audio_info(self, audio_ids):
        api_response = {"has_errors": False, "result": None}
        ids = ','.join(str(x) for x in audio_ids)
        headers = {"cookie": self.__cookie}
        params = {"act": "reload_audio", "al": 1, "ids": ids}

        audio_info = self.__get_response(headers, params)
        if audio_info is None:
            api_response["has_errors"] = True
            api_response["error_description"] = "Cookie has expired"
            return json.dumps(api_response)

        result = []

        for item in audio_info:
            track_id = item[1] + "_" + item[0]
            link = item[2]
            result.append({"track_id": track_id, "link": link})

        if len(result) == 1:
            api_response['result'] = result[0]
        else:
            api_response['result'] = result

        return json.dumps(api_response)

    def get_audio_list(self, owner_id):
        api_response = {"has_errors": False, "result": None}
        headers = {"cookie": self.__cookie}
        params = {"act": "load_silent", "al": 1, "album_id": -2, "band": False, "owner_id": owner_id}

        j_object = self.__get_response(headers, params)
        if j_object is None:
            api_response["has_errors"] = True
            api_response["error_description"] = "Cookie has expired"
            return json.dumps(api_response)

        audio_list = j_object['list']

        result = []

        for item in audio_list:
            track_id = item[1] + "_" + item[0]
            title = self.__parser.unescape(item[4] + " - " + item[3])
            result.append({"track_id": track_id, "title": title})

        api_response['result'] = result

        return json.dumps(api_response)

    def search(self, query):
        api_response = {"has_errors": False, "result": None}
        headers = {"cookie": self.__cookie}
        params = {"act": "a_load_section", "al": 1, "claim": 0, "offset": 0, "search_history": 1, "search_lyrics": 0, 
        "search_performer": 0, "search_q": query, "search_sort": 0, "type": "search"}

        j_object = self.__get_response(headers, params)
        if j_object is None:
            api_response["has_errors"] = True
            api_response["error_description"] = "Cookie has expired"
            return json.dumps(api_response)

        audio_list = j_object['list']

        result = []

        for item in audio_list:
            track_id = item[1] + "_" + item[0]
            title = self.__parser.unescape(item[4] + " - " + item[3])
            result.append({"track_id": track_id, "title": title})

        api_response['result'] = result

        return json.dumps(api_response)

    def __get_response(self, headers, params):
        resp = self.__client.post(self.__url, headers, params)

        match = re.search('<!json>(.*?)(<!>)', resp.content)
        if match is None:
            return None

        j_str = unicode(match.group(1), 'cp1251')

        return json.loads(j_str)