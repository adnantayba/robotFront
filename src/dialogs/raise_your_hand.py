from commands.RRA import RRA
from botbuilder.dialogs import (
    WaterfallStepContext,
    DialogTurnResult,
    WaterfallDialog
)
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from .cancel_and_help_dialog import CancelAndHelpDialog 
from botbuilder.schema import InputHints
from classes.classes import rra, language
import json
#from sklearn.preprocessing import LabelEncoder
from ml_models.side_model.side_model import svm_model, tf_idf, label_encoder

from .number_extraction_function import extract_number
from translate import translateToEnglish, replace_word, translateToArabic
#import pickle
#from bert_model import get_sentence_embedding

"""
This is the dialog that handles the Raise_Your_Hand intent dialog.
It checks if there's any missing entities by checking the rra attributes and it goes step by step to check them all.
In the degree missing entity, it checks if we enter a right sentence by using the SVM classification model.
Then it extracts the number from our sentence and fill it in the entity using extract_number function.
Finally when all the entities are filled, it confirm the dialog by sending the json response and ending the dialog.
"""
# Load the SVM model for degree detection
# with open('svm_model.pkl', 'rb') as file:
#     loaded_svm_model = pickle.load(file)

def replace_monday(sentence):
    if 'Monday' in sentence:
        return sentence.replace('Monday', 'to raise your both hands')
    else:
        return sentence

class Raise_Your_Hand(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(Raise_Your_Hand, self).__init__(dialog_id or Raise_Your_Hand.__name__)
        self.prediction = None

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [   self.side_step,
                    self.degree_step,
                    self.duration_step,
                    self.confirm, 
                    self.acknowledgement_step
                ]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__       
        self.USER_INFO = rra  
        
    async def side_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if self.USER_INFO.side is None:
            if language.language == "en" or language.language == "fr":
                message_text = "My left hand or the right one?"
            else :
                message_text = "بَدَكْ إيدي اليَمينْ اوْ الشْمالْ؟"
            json_data = {"text" : message_text}
            json_data = json.dumps(json_data)
            prompt_message = MessageFactory.text(
                json_data, json_data, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(self.USER_INFO.side)

    async def degree_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Fill in the side value
        # check if there's missing entity:
        test_sentences = [translateToEnglish(step_context.result)]
        # Predict if it's a valid degree sentence or not using the loaded SVM model
        text_to_predict_embedding = tf_idf.transform(test_sentences)
        predicted_label = svm_model.predict(text_to_predict_embedding)
        predicted_category = label_encoder.inverse_transform(predicted_label)
        self.USER_INFO.side = predicted_category[0]
        # check if there's missing entity
        if self.USER_INFO.degree is None:
            # if language.language == "en" or language.language == "fr":
            #     message_text = "Please provide me with the degree"
            # else:
            #     self.USER_INFO.side = translateToEnglish(step_context.result)
            #     self.USER_INFO.side = replace_word(self.USER_INFO.side, 'North', 'left')
            #     message_text = "على أي زاويه بَدَكْ ياني أِرْفَعْ إيدي"
            self.USER_INFO.degree = "150 degrees"
            # send the message text to the user
        #     json_data = {"text" : message_text}
        #     json_data = json.dumps(json_data)
        #     prompt_message = MessageFactory.text(
        #         json_data, json_data, InputHints.expecting_input
        #     )
        #     return await step_context.prompt(
        #         TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        #     )
        # # this is the case when enter a not valid degree sentence
        # elif self.USER_INFO.degree == 'this is not a valid degree value, re-enter a valid degree value please' or self.USER_INFO.degree == "هيدي القِيِمِه مِشْ صَحيحه، اِرْجاعْ اعْطيني الزاوْيه بِشَكْلْ صحيحْ":
        #     message_text = self.USER_INFO.degree
        #     json_data = {"text" : message_text}
        #     json_data = json.dumps(json_data)
        #     self.USER_INFO.degree = None
        #     prompt_message = MessageFactory.text(
        #         # expecting_input for the inputhints to be sent to the frontend side in order to determine the state based on the InputHints value
        #         json_data, json_data, InputHints.expecting_input
        #     )
        #     return await step_context.prompt(
        #         TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        #     )
        # the degree is filled
        return await step_context.next(self.USER_INFO.degree)

    async def duration_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # Fill in the degree value by the number extracted
        # question = ast.literal_eval(step_context.result)


        # check if there's missing entity:
        self.USER_INFO.degree = translateToEnglish(step_context.result)
        self.USER_INFO.degree = extract_number(self.USER_INFO.degree)
        # self.USER_INFO.degree = extract_number(question[0])
        # Predict if it's a valid degree sentence or not using the loaded SVM model
        # test_sentences = [translateToEnglish(step_context.result)]
        # # Predict if it's a valid degree sentence or not using the loaded SVM model
        # test_sentences = get_sentence_embedding(test_sentences)
        # y_pred = loaded_svm_model.predict(test_sentences)
        # print(y_pred[0])
        # self.USER_INFO.degree = extract_number(self.USER_INFO.degree)
        # # 0: not valid, 1: valid
        # if y_pred[0] == 0:
        #     # this is for the condition in the degree_step function
        #     if language.language == 'en' or language.language == "fr":
        #         self.USER_INFO.degree = 'this is not a valid degree value, re-enter a valid degree value please'
        #     else:
        #         self.USER_INFO.degree = "هيدي القِيِمِه مِشْ صَحيحه، اِرْجاعْ اعْطيني الزاوْيه بِشَكْلْ صحيحْ"
        #     # end the old dialog
        #     await step_context.end_dialog()
        #     # begin a new dialog
        #     return await step_context.begin_dialog(Raise_Your_Hand.__name__)

        # check the duration entity
        if self.USER_INFO.duration is None:
            # if language.language == 'en' or language.language == "fr":
            #     message_text = "For how long do you want me to raise my hand?"
            # else:
            #     message_text = "لَءَّديشْ وَءِتْ بَدَكْ ياني ضَّلْني رافِعْ إيدي"
            # json_data = {"text" : message_text}
            # # send the message text
            # json_data = json.dumps(json_data)
            # prompt_message = MessageFactory.text(
            #     json_data, json_data, InputHints.expecting_input
            # )
            # return await step_context.prompt(
            #     TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            # )
            self.USER_INFO.duration = '5 seconds'
        return await step_context.next(self.USER_INFO.duration)

    
    async def confirm(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # fill in the duration entity value
        # question = ast.literal_eval(step_context.result)
        # self.USER_INFO.duration = question[0]

        self.USER_INFO.duration = translateToEnglish(step_context.result)
        self.USER_INFO.duration = extract_number(self.USER_INFO.duration)
        # enter the speech text attribute in a dynamic way based on the side value
        if language.language == 'en' or language.language == "fr":
            self.USER_INFO.text = f"I'm raising my {self.USER_INFO.side} hand"
        else:
            self.USER_INFO.duration = translateToEnglish(step_context.result)
            self.USER_INFO.text = f"أنا عَمْ عََلّي إيدي {translateToArabic(self.USER_INFO.side)}"
        json_data = self.USER_INFO.to_json()
        prompt_message = MessageFactory.text(
                json_data, json_data, InputHints.accepting_input
            )
        return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
    # end the dialog
    async def acknowledgement_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        return await step_context.end_dialog()
