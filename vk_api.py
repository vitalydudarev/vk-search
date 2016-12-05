import urllib
import json

class VkApi:
    def __init__(self, access_token):
        self.__uri = "https://api.vk.com/method/"
        self.__access_token = access_token
        self.__api_version = "5.60"

    # https://api.vk.com/method/audio.search?v=5.60&access_token=0267407ef17542413c1883d1681a1aff6d07b8a8c2e24be83b0ad85606645d24a30d78f6ba057bd7ee45b&q=Armin%20van%20buuren
    def search(self, q):
        method_name = "audio.search"
        uri = self.__uri + method_name + "?v=" + self.__api_version\
         + "&access_token=" + self.__access_token + "&q=" + q
        response = self.__get_response(uri)
        #return response
        json_r = json.loads(response)
        item_one = json_r["response"]["items"][0]
        return str(item_one["artist"]) + " - " + item_one["title"]

    def __get_response(self, url):
        u = urllib.urlopen(url)
        return u.read()