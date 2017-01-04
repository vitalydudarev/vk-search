class Storage:
    def __init__(self):
        self.__dict = {}

    def add(self, key, value):
        self.__dict[key] = value

    def get(self, key):
        if key in self.__dict:
            return self.__dict[key]
        return None