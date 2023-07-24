from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus
from botbuilder.core import StatePropertyAccessor, TurnContext

class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog, turn_context: TurnContext, accessor: StatePropertyAccessor
    ):
        dialog_set = DialogSet(accessor)
        # Add the WaterfallDialog to the DialogSet
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        print(results, "helper dialog")
        if results.status == DialogTurnStatus.Empty:
            # Begin the WaterfallDialog by providing its dialog ID
            await dialog_context.begin_dialog(dialog.id)