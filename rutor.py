import json
import os.path


class RutorDataHolder:

    __data = {}

    def __init__(self, file_name):
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                data = json.loads(file.read())
                res = [dict(t) for t in set([tuple(d.items()) for d in data])]
                self.__data = sorted(res, key=lambda k: k['torrent_id'], reverse=True)

    def get_data(self, index=0):
        result = [self.__data[i] for i in range(index, index + 100)]
        return json.dumps(result, cls=Encoder)


class Encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__
