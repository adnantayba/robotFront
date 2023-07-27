
# LUIS configuration

# from commands.RRA import RRA

# rra = RRA()

# import libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

from config import DefaultConfig
CONFIG = DefaultConfig()

async def sample_analyze_orchestration_app_luis_response(query):  
    client = ConversationAnalysisClient(CONFIG.clu_endpoint, AzureKeyCredential(CONFIG.clu_key))
    with client:
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": CONFIG.project_name,
                    "deploymentName": CONFIG.deployment_name,
                    "verbose": True
                }
            }
        )
    return result


