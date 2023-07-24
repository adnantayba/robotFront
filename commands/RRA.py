# Raise your arm class for its intent

import json
class RRA():

    def __init__(self):
        self.degree = None
        self.duration = None
        self.intent = None
        self.side = None
        self.text = f"I'm raising my {self.side} hand"

    def to_json(self):
        data = {
            "intent" : self.intent,
            "entities" : {
            "side": self.side,
            "duration": self.duration,
            "degree": self.degree},
            "text": self.text
        }
        return json.dumps(data)
    
    def clear_entities(self):
        if self.degree is not None and self.duration is not None and self.side is not None:
            self.degree = None
            self.duration = None
            self.side = None
