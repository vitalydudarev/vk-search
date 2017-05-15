from vk_audio import VkAudio
from client import HttpClient
import json

client = HttpClient(timeout=10)
api = VkAudio('remixsid=', client)

print api.get_playlist(20442343)
print api.search('armin van buuren')