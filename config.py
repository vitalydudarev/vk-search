import json


class Config:
    def __init__(self):
        self.access_token = ''
        self.proxy = []
        self.user_id = 0

def get_item(data, key, default_value):
    if key in data:
        return data[key]
    else:
        return default_value

def load_config(file_name):
    with open(file_name) as json_data:
        data = json.load(json_data)

        config = Config()
        config.access_token = get_item(data, 'access_token', '')
        config.proxy = get_item(data, 'proxy', {})
        config.user_id = get_item(data, 'user_id', 0)

        return config