#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    # Bot configuration
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "81c2c34e-2754-4f0e-b1f2-335bdd348c80")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "Qtn8Q~Qdxhl4lyIKKrZxKTlhlq5EtmSnkcT-jbao")

    # Qna configuration 
    ENDPOINT = os.environ.get("EndPoint","https://qnachatbotrobot.cognitiveservices.azure.com/")
    KEY = os.environ.get("key", "75d2b38778614a8cb890d94a70cc903d")
    KNOWLEDGE_BASE_PROJECT = os.environ.get("KnowledgeBaseProject", "PersonalQuestions")

    # LUIS configuration
    clu_endpoint = os.environ.get("clu_endpoint", "https://luischatbotrobot.cognitiveservices.azure.com/")
    clu_key = os.environ.get("clu_key", "7c902bbbc9384fae9ff3d4437f09278b")
    project_name = os.environ.get("clu_project_name", "Actionable_Robot")
    deployment_name = os.environ.get("clu_deployment_name", "deploy_luis")

    # Translator configuration
    TRANSLATOR_KEY = '1fa4763606654a72b6b11a04b7cd0a4f'
    TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
    TRANSLATOR_REGION = 'global'

    # OpenAi key
    OPENAI_KEY = ' '

