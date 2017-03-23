import json


class ApiResponse:
    def __init__(self, has_error=False, error_description='', result=None):
        self.has_error = has_error
        self.error_description = error_description
        self.result = result

    def to_json(self):
        return json.dumps(self.__dict__)
