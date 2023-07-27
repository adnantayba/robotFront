from botbuilder.dialogs import (
    WaterfallStepContext,
    DialogTurnResult,
    WaterfallDialog
)
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from .cancel_and_help_dialog import CancelAndHelpDialog 
from botbuilder.schema import InputHints
import pickle
from bert_model import get_sentence_embedding
from translate import translateToEnglish
import spacy

with open('confirm_model.pkl', 'rb') as file:
    loaded_svm_model = pickle.load(file)

nlp1 = spacy.load(r".\output\model-best")

import json
from classes.classes import face_name, language

"""
This dialog handles the Ask_Your_Name intent dialog. It checks if there are any missing entities by checking the `USER_INFO` attributes and goes step by step to check them all.

The dialog includes the following steps:
1. `name_step`: This step prompts the user to provide their name if it is missing. It expects the user to enter their name.
2. `name_confirm_step`: This step fills in the `USER_INFO.name` entity value by extracting it using the Spacy model. If the name entity is not detected, it ends the current dialog and starts a new dialog. It then prompts the user to confirm their name.
3. `confirm`: This step uses an SVM classification model (`loaded_svm_model`) to determine if the user's confirmation sentence is valid. If the model predicts that the sentence does not confirm the name, it resets the `USER_INFO.name` entity to None, ends the current dialog, and starts a new dialog. Otherwise, it sets the `USER_INFO.text` attribute with a greeting message addressed to the user.
4. `acknowledgement_step`: This step ends the dialog.

The `Ask_Your_Name` class inherits from the `CancelAndHelpDialog` class and initializes the necessary dialogs and dialog IDs.
"""

def add_name_to_sentence(sentence):
    sentence_list = sentence.split()

    # Check if the length of the sentence is less than or equal to 2
    if len(sentence_list) <= 2:
        sentence_list.insert(0, "اسمي")  # Insert "اسمي" at the beginning of the list

    new_sentence = " ".join(sentence_list)  # Convert the list back to a string with space-separated elements
    return new_sentence

class Ask_Your_Name(CancelAndHelpDialog):

    def __init__(self, dialog_id: str = None):
        super(Ask_Your_Name, self).__init__(dialog_id or Ask_Your_Name.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__+"2",
                [  
                    self.name_step,
                    self.name_confirm_step,
                    self.confirm, 
                    self.acknowledgement_step
                ]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__+"2"   
        self.USER_INFO = face_name  

    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if self.USER_INFO.name is None:
            if language.language == "en" or language.language == "fr":
                message_text = "What's your name?"
            else:
                message_text = "شو إِسْمَكْ؟"
            json_data = {"text" : message_text}
            json_data = json.dumps(json_data)
            prompt_message = MessageFactory.text(
                json_data, json_data, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(self.USER_INFO.name)
    
    async def name_confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # fill in the name entity value
        text = step_context.result
        if language.language == "ar" or language.language== "fa":
            text = add_name_to_sentence(step_context.result)
        self.USER_INFO.name = nlp1(translateToEnglish(text))
        self.USER_INFO.name = str(self.USER_INFO.name.ents[0])
        if len(self.USER_INFO.name) == 0:
            # end the old dialog
            await step_context.end_dialog()
            # begin a new dialog
            return await step_context.begin_dialog(Ask_Your_Name.__name__)
        # enter the speech text attribute in a dynamic way based on the name value
        if language.language == "en" or language.language == "fr":
            message_text = {
                "text": f"are your sure your name is {self.USER_INFO.name}?"
            } 
        else:
            message_text = {
                "text": f"مِتْأَكَدْ إنّو إسْمَكْ  {self.USER_INFO.name}؟"
            }
        json_data= json.dumps(message_text)
        prompt_message = MessageFactory.text(
                json_data, json_data, InputHints.expecting_input
            )
        return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

    async def confirm(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        confirm = step_context.result
        confirm = translateToEnglish(confirm)
        test_sentence = get_sentence_embedding([confirm])
        y_pred = loaded_svm_model.predict(test_sentence)
        if y_pred[0] == 0:
            self.USER_INFO.name = None
            # end the old dialog
            await step_context.end_dialog()
            # begin a new dialog
            return await step_context.begin_dialog(Ask_Your_Name.__name__)
        if language.language == "en" or language.language == "fr":
            self.USER_INFO.text = f"Hey {self.USER_INFO.name}, nice to meet you"
        else:
            self.USER_INFO.text = f"مَرْحَباَ  {self.USER_INFO.name}, تِشِرَّفِتْ  بِمَعْرِفْتَكْ"
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
        
