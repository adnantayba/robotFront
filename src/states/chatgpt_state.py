import json
from helpers.gpt3_api_helper import GPT3
gpt3 = GPT3()
from classes.classes import language
from botbuilder.dialogs.prompts import PromptOptions
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory

async def connect_to_chatgpt(question):
    # # Connect to ChatGPT and get the response
    # chatgpt_response = await gpt3.gpt3(question)
    if language.language == 'en' or language.language == 'fr':
        json_data = {"text" : "I'm not able to answer to this"}
    else:
        json_data = {'text' : "بَعدْني مِشْ جاهِزْ تَ جاوِبْ عَ هيك شي"}
    json_data = json.dumps(json_data)
    prompt_options = PromptOptions(
    prompt=MessageFactory.text(json_data,input_hint=InputHints.accepting_input),
    )
    return prompt_options
