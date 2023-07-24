from botbuilder.dialogs import (
    WaterfallStepContext,
    DialogTurnResult,
    WaterfallDialog
)
from botbuilder.core import MessageFactory
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from dialogs.cancel_and_help_dialog import CancelAndHelpDialog 
from botbuilder.schema import InputHints

from classes import mmhm, language

"""
this intent doesn't have entities, so we don't need additional step other than confirming.
it goes directly to the end of the dialog after sending the response back
"""

class Mimic_My_Hand_Movement(CancelAndHelpDialog):

    def __init__(self, dialog_id: str = None):
        super(Mimic_My_Hand_Movement, self).__init__(dialog_id or Mimic_My_Hand_Movement.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            # create the waterfall dialog
            WaterfallDialog(
                WaterfallDialog.__name__+"1",
                [   self.confirm,
                    self.acknowledgement_step
                ]
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__+"1"
        self.USER_INFO = mmhm  


    async def confirm(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        print(language.language, "arabic1")
        if language.language == "en":
            print(language.language, "arabic2")
            self.USER_INFO.text = f"I'm mimicking your hand movement" 
        else:
            self.USER_INFO.text = f"ليكْ انا كمان عم حَرِّكْ ايدي مِتْلَكْ"
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
