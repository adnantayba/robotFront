from botbuilder.dialogs import (
    ComponentDialog,
    DialogContext,
    DialogTurnResult
)
from botbuilder.schema import ActivityTypes, InputHints
from botbuilder.core import MessageFactory
import json


class CancelAndHelpDialog(ComponentDialog):
    def __init__(self, dialog_id: str):
        super(CancelAndHelpDialog, self).__init__(dialog_id)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        # Check if the current activity is an interrupting message
        result = await self.interrupt(inner_dc)
        if result is not None:
            return result
        # Continue the dialog if no interruption occurred
        return await super(CancelAndHelpDialog, self).on_continue_dialog(inner_dc)

    async def interrupt(self, inner_dc: DialogContext) -> DialogTurnResult:
        if inner_dc.context.activity.type == ActivityTypes.message:
            # Retrieve the text from the user's message and convert it to lowercase
            text = inner_dc.context.activity.text.lower()

            # Create a cancel message
            cancel_message_text = "Cancelling"
            cancel_message_text = {"text" : cancel_message_text}
            cancel_message_text = json.dumps(cancel_message_text)
            cancel_message = MessageFactory.text(
                cancel_message_text, cancel_message_text, InputHints.ignoring_input
            )

            # Check if the user's message indicates cancellation
            if text in ("cancel", "quit", "back to initial state", "stop"):
                # Send the cancel message to the user
                await inner_dc.context.send_activity(cancel_message)
                # Cancel all dialogs and return to the parent dialog
                return await inner_dc.parent.cancel_all_dialogs()
            
        # No interruption occurred
        return None