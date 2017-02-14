import json
from client import Response


class VkApi:
    def __init__(self, access_token, client):
        self.__uri = "https://api.vk.com/method/"
        self.__access_token = access_token
        self.__api_version = "5.60"
        self.__client = client

    def search(self, q):
        method_name = "audio.search"
        uri = self.__uri + method_name + "?v=" + self.__api_version + "&access_token=" + self.__access_token + "&q=" + q
        uri = uri.replace(' ', '%20')

        response = self.__client.get_response(uri)
        json_result = json.loads(response.response_text)
        if 'error' in json_result:
            return json.dumps([])

        result = []

        for item in json_result["response"]["items"]:
            audio = Audio(item["artist"] + " - " + item["title"], item["url"])
            result.append(audio)

        return json.dumps(result, cls=AudioJsonEncoder)

    def get_audio(self, owner_id):
        method_name = "audio.get"
        uri = self.__uri + method_name + "?v=" + self.__api_version + "&access_token=" + self.__access_token + "&owner_id=" + str(owner_id)
        uri = uri.replace(' ', '%20')

        response = self.__client.get_response(uri)
        json_result = json.loads(response.response_text)
        if 'error' in json_result:
            return json.dumps([])

        result = []

        for item in json_result["response"]["items"]:
            audio = Audio(item["artist"] + " - " + item["title"], item["url"])
            result.append(audio)

        return json.dumps(result, cls=AudioJsonEncoder)

class Audio(object):
    def __init__(self, title, link):
        self.title = title
        self.link = link

class AudioJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Audio):
            return obj.__dict__
        return obj