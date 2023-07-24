# face name class for its intent
import json



class Face_Name():

    def __init__(self):
        self.intent = None
        self.name = None
        
        self.text = f"Hey {self.name}, nice to meet you"

    def to_json(self):
        data = {
            "intent" : self.intent,
            "entities" : {
            "name": self.name},
            "text": self.text
        }
        return json.dumps(data)

    def clear_entities(self):
        if self.name is not None:
            self.name = None