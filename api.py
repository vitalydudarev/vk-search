import json
import re

class JsonSerializable(object):
    CAMEL_PATTERN = re.compile(r'([A-Z])')
    SNAKE_PATTERN = re.compile(r'_([a-z])')

    def camel_to_snake(self, name):
        return self.CAMEL_PATTERN.sub(lambda x: '_' + x.group(1).lower(), name)

    def snake_to_camel(self, name):
        return self.SNAKE_PATTERN.sub(lambda x: x.group(1).upper(), name)

    def to_json(self):
        return json.dumps({self.snake_to_camel(k): v for k, v in self.__dict__.items()})

    def from_json(self, s):
        obj = json.loads(s)
        self.__dict__ = {self.camel_to_snake(k): v for k, v in obj.items()}
        return self

class ApiResponse(JsonSerializable):
    def __init__(self, has_error=False, error_description='', result=None):
        self.has_error = has_error
        self.error_description = error_description
        self.result = result
