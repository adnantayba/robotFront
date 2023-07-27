import openai
from config import DefaultConfig
CONFIG = DefaultConfig()

openai.api_key = CONFIG.OPENAI_KEY

class GPT3():
    @staticmethod
    async def gpt3(stext):
        # Make a request to the GPT-3 model
            messages = [
            {"role": "user", "content": 'Hello, assistant!'},
            {"role": "assistant", "content": 'Hello! How can I assist you today?'},
            {"role": "user", "content" : stext}
            ]

            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            )
            print(response['choices'][0]['message']['content'])
            return response['choices'][0]['message']['content']
        
        # Split the response into separate sentences
        #content = response.choices[0].message.content.split('.')
        #print(content)
        #print(response)
        #return response['choices'][0]['message']['content']
