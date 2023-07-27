from botbuilder.dialogs import (
    WaterfallStepContext,
    DialogTurnResult,
    WaterfallDialog
)
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from dialogs.cancel_and_help_dialog import CancelAndHelpDialog 
from botbuilder.schema import InputHints

from classes.classes import greetings, language

"""
this intent doesn't have entities, so we don't need additional step other than confirming.
it goes directly to the end of the dialog after sending the response back
"""

class Greetings(CancelAndHelpDialog):

    def __init__(self, dialog_id: str = None):
        super(Greetings, self).__init__(dialog_id or Greetings.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            # create the waterfall dialog
            WaterfallDialog(
                WaterfallDialog.__name__+"3",
                [   self.confirm,
                    self.acknowledgement_step
                ]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__+"3"
        self.USER_INFO = greetings  


    async def confirm(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if language.language == "ar" or language.language == 'fa':
            self.USER_INFO.text = f"أهليٍنْ أهليٍنْ"
        else:
            self.USER_INFO.text = f"Hey there!" 
        json_data = self.USER_INFO.to_json()
        prompt_message = MessageFactory.text(
                json_data, json_data, InputHints.accepting_input
            )
        return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

    async def acknowledgement_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        
        return await step_context.end_dialog()
