# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import sys
import traceback
from datetime import datetime

from flask import Flask, request, jsonify

from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    MemoryStorage,
    ConversationState,
    UserState,
    BotFrameworkAdapter,
)
from botbuilder.schema import Activity, ActivityTypes
from bot import MyBot

from dialogs.main_dialog import MainDialog
from dialogs.raise_your_hand import Raise_Your_Hand
from dialogs.mimic_my_hand_movement import Mimic_My_Hand_Movement
from dialogs.ask_your_name import Ask_Your_Name

from config import DefaultConfig
CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Create MemoryStorage and state
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

# Create Dialog and Bot
top_dialog = Raise_Your_Hand()
mimic_my_hand_movement = Mimic_My_Hand_Movement()
ask_your_name = Ask_Your_Name()
DIALOG = MainDialog(top_dialog, mimic_my_hand_movement,ask_your_name, USER_STATE)
BOT = MyBot(CONVERSATION_STATE, USER_STATE, DIALOG)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Listen for incoming requests on /api/messages
app = Flask(__name__)


@app.route('/api/messages', methods=['POST'])
async def messages():
    # Main bot message handler.
    if "application/json" in request.headers.get("Content-Type"):
        body = request.get_json()
    else:
        return '', 415

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    try:
        response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
        if response:
            return jsonify(response.body), response.status
        return '', 201
    except Exception as exception:
        raise exception


if __name__ == "__main__":
    try:
        app.run(host='localhost', port=CONFIG.PORT)
    except Exception as error:
        raise error