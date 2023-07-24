from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)

from botbuilder.dialogs.prompts import TextPrompt

from dialogs.raise_your_hand import Raise_Your_Hand
from dialogs.mimic_my_hand_movement import Mimic_My_Hand_Movement
from dialogs.ask_your_name import Ask_Your_Name

from config import DefaultConfig
from states.chatgpt_state import connect_to_chatgpt
from states.luis.luis_state import connect_to_luis, connect_to_luis_rra, connect_to_luis_face_name
from states.qna.qna_config import connect_to_qna
from states.qna.qna_state import send_qna_answer
#from states.rasa_state import connect_to_rasa
from classes import rra, mmhm, face_name, language

CONFIG = DefaultConfig()

from language_detect import detect_language

from translate import translateToEnglish, replace_word



class MainDialog(ComponentDialog):

    """
    The main dialog class that orchestrates the conversation flow.
    """

    def __init__(
        self, raise_your_hand_dialog: Raise_Your_Hand, mimic_my_hand_movement: Mimic_My_Hand_Movement, ask_your_name: Ask_Your_Name, user_state
    ):
        """
        Initializes the MainDialog.

        Args:
            raise_your_hand_dialog (Raise_Your_Hand): The dialog for raising hand.
            mimic_my_hand_movement (Mimic_My_Hand_Movement): The dialog for mimicking hand movement.
            ask_your_name (Ask_Your_Name): The dialog for asking user's name.
            user_state: The user's state.

        """
        super(MainDialog, self).__init__(MainDialog.__name__)
        self._top_dialog_id = raise_your_hand_dialog.id
        self._mimic_my_hand_movement_id = mimic_my_hand_movement.id
        self._ask_your_name_id = ask_your_name.id
        self.user_state = user_state
        # Add necessary dialogs
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(raise_your_hand_dialog)
        self.add_dialog(mimic_my_hand_movement)
        self.add_dialog(ask_your_name)
        # Build the waterfall dialog (the main dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.initial_step, self.intent_detection_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        This step is the entry point of the dialog and simply passes control to the next step.
        """
        return await step_context.next([])
    
    async def intent_detection_step(
            self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        This step performs intent detection and determines the appropriate action to take based on the user's input.

        It first checks if the user's question can be answered using QnA Maker. If the confidence level is high enough, it prompts the user with the answer.

        If the confidence level is below 0.8, the dialog connects to LUIS to identify the user's intent and takes the corresponding action.

        If the intent is "Raise_Your_Hand", it connects to LUIS to extract any missing entities and starts the "Raise_Your_Hand" dialog.

        If the intent is "mimic_my_hand_movement", it fills in the class mmhm attributes with the extracted intent and starts the "Mimic_My_Hand_Movement" dialog.

        If the intent is "ask_your_name", it connects to LUIS to extract any missing entities and starts the "Ask_Your_Name" dialog.

        If the intent confidence is below 0.9, it connects to ChatGPT for a response.

        Args:
            step_context (WaterfallStepContext): The context of the current step.

        Returns:
            DialogTurnResult: The result of the current step.
        """



        question = step_context.context.activity.text 
        #question = ast.literal_eval(question)
        question_language = detect_language(question)
        print(question_language, "language")
        language.language = question_language

        # # Send the POST request to the RASA server
        # prompt_options = connect_to_rasa(question)
        # return await step_context.prompt(
        #     TextPrompt.__name__, prompt_options
        # )
        
        # connect to QnA
        # Send the POST request to the QnA Servcice
    
        output = await connect_to_qna(question)
        if output.answers:
            for a in output.answers:
                #checking the confidence of the QnA and making a condition
                if a.confidence > 0.7:
                    prompt_options, confidence = await send_qna_answer(a)
                    return await step_context.prompt(
                        TextPrompt.__name__, prompt_options
                    )
                # Go to LUIS since the confidence level in QnA is below 0.8
                else:
                    # connect to LUIS
                    replaced_sentence = replace_word(question, 'الشمال', 'اليسار')
                    translate_to_english = translateToEnglish(replaced_sentence)
                    print(translate_to_english, "enen")
                    replaced_sentence = replace_word(translate_to_english, 'North', 'left')
                    print(replaced_sentence, "replaced")
                    if language.language == 'en' or language.language == 'fr':
                        top_intent, intent_response, confidence =await connect_to_luis(question)
                    else:
                        top_intent, intent_response, confidence =await connect_to_luis(replaced_sentence)
                    
                    if confidence > 0.8:
                        # check if the intent is 'Raise_Your_Hand'
                        if top_intent == "Raise_Your_Hand": 
                            await connect_to_luis_rra(top_intent, intent_response, rra)
                            # begin the dialog to check if there's missing entities
                            return await step_context.begin_dialog(Raise_Your_Hand.__name__)
                        # check if the intent is 'mimic_my_hand_movement'
                        elif top_intent == "mimic_my_hand_movement": 
                            # fill in the class mmhm attributes with the extracted intent
                            mmhm.intent = top_intent
                            return await step_context.begin_dialog(Mimic_My_Hand_Movement.__name__)
                        elif top_intent == "ask_your_name":
                            await connect_to_luis_face_name(top_intent, intent_response, face_name)
                            return await step_context.begin_dialog(Ask_Your_Name.__name__)

                    else:
                        prompt_options = await connect_to_chatgpt(question)
                        return await step_context.prompt(
                            TextPrompt.__name__, prompt_options
                        )
                            
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        This step ends the dialog and replaces it with a new instance of the MainDialog, allowing for a new conversation.
        """
        return await step_context.replace_dialog(MainDialog.__name__)

 