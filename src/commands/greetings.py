# Mimic my hand movement class for its intent

import json
class Greetings():

    def __init__(self):
        self.intent = None
        self.text = f"Hey there!"

    def to_json(self):
        data = {
            "intent" : self.intent,
            "text": self.text
        }
        return json.dumps(data)
