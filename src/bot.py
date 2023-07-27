from botbuilder.schema import ChannelAccount

from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper

class MyBot(ActivityHandler):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,):
        if conversation_state is None:
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_message_activity(self, turn_context: TurnContext):
        # run the dialog
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

    # send the first message (welcome message) to make sure of connection to the bot            
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
                print("new member added")
