# import libraries
from config import DefaultConfig
CONFIG = DefaultConfig()

from azure.ai.language.questionanswering.aio import QuestionAnsweringClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import models as qna

async def connect_to_qna(question):   
    """
    Connects to the Azure QnA Maker service and retrieves answers for a given question.

    Args:
        question (str): The question to be answered.

    Returns:
        qna.QuestionAnsweringModel: The QnA response containing the answer(s) to the question.

    """
    # Connect to the QnA Maker service
    client = QuestionAnsweringClient(CONFIG.ENDPOINT, AzureKeyCredential(CONFIG.KEY))
    async with client:
        # QnA configuration
        output = await client.get_answers(
            question=question,
            top=3,
            confidence_threshold=0.2,
            include_unstructured_sources=True,
            short_answer_options=qna.ShortAnswerOptions(
                confidence_threshold=0.2,
                top=1
            ),
            project_name=CONFIG.KNOWLEDGE_BASE_PROJECT,
            deployment_name="test"
        )
    
    return output


