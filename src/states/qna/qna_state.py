import json
from botbuilder.dialogs.prompts import PromptOptions
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory

async def send_qna_answer(a):
    """
    Sends a Q&A answer to the user.

    Args:
        a (QnAResult): The Q&A result containing the answer.

    Returns:
        tuple: A tuple containing the prompt options and the confidence score.

    """
    # Select the best candidate answer
    best_candidate = a

    # Get the answer text from the best candidate
    answer = best_candidate.answer

    # Compress the response into a JSON format
    json_data_qna = {"text": answer}
    json_data_qna = json.dumps(json_data_qna)

    # Create the prompt options with the JSON response as the prompt message
    prompt_options = PromptOptions(
        prompt=MessageFactory.text(json_data_qna, input_hint=InputHints.accepting_input)
    )

    # Return the prompt options and the confidence score
    return prompt_options, a.confidence
