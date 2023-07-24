from states.luis.luis_config import sample_analyze_orchestration_app_luis_response
from classes import rra, face_name, language
from translate import translateToEnglish

async def connect_to_luis(question):
    # Clear the class rra (Raise arm) so we avoid conflicts 
    rra.clear_entities()
    face_name.clear_entities()
    # connect to LUIS
    intent_reponse = await sample_analyze_orchestration_app_luis_response(question)
    # check the confidence level
    top_intent = intent_reponse["result"]["prediction"]["topIntent"]
    return top_intent, intent_reponse, intent_reponse["result"]["prediction"]['intents'][0]['confidenceScore']

async def connect_to_luis_rra(top_intent, intent_reponse, rra):
        #fill in the class rra attributes with the extracted intent and entities
        rra.intent = top_intent
        entities = intent_reponse["result"]["prediction"]["entities"]
        for i in range(len(entities)):
            if entities[i]['category'] == 'side':
                rra.side = entities[i]['text']
                rra.text = f"I'm raising my {rra.side} hand"
            elif entities[i]['category'] == 'degree':
                rra.degree = entities[i]['text']
            else:
                rra.duration = entities[i]['text']

async def connect_to_luis_face_name(top_intent, intent_reponse, face_name):
    face_name.intent = top_intent
    entities = intent_reponse["result"]["prediction"]["entities"]
    for i in range(len(entities)):
        face_name.name = entities[i]['text']
        face_name.text = f"Hey {face_name.name}, nice to meet you"
