

class JSONTemplate:
    def __init__(self, data: dict):
        self.languages = dict.get('language')
        self.fields = data.get('fields')
