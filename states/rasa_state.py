import requests, json
from botbuilder.dialogs.prompts import  PromptOptions
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory
async def connect_to_rasa(question):
    payload = {

                "sender": "user1",
                "message": question
            }
    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json=payload)
    dictionary = json.loads(r.json()[0]['text'])
    prompt_options = PromptOptions(
    prompt=MessageFactory.text(dictionary,input_hint=InputHints.accepting_input),
    )
    return prompt_options