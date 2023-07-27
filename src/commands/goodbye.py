# Mimic my hand movement class for its intent

import json
class Goodbye():

    def __init__(self):
        self.intent = None
        self.text = f"Bye Bye"

    def to_json(self):
        data = {
            "intent" : self.intent,
            "text": self.text
        }
        return json.dumps(data)
