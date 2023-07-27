# Mimic my hand movement class for its intent

import json
class MMHM():

    def __init__(self):
        self.intent = None
        self.text = f"I'm mimicing your hand movement"

    def to_json(self):
        data = {
            "intent" : self.intent,
            "text": self.text
        }
        return json.dumps(data)
