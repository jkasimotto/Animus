import json
from enum import Enum
from textwrap import dedent
from typing import List

import firebase_admin
import functions_framework
from db.Firestore import Firestore
from db.Weaviate import Weaviate
from firebase_admin import credentials, firestore
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from models.Conversation import Conversation
from Animus import Animus

# from firebase_admin import auth


@functions_framework.http
def agent(request):

    # Connect to Firestore and Weaviate databases
    weaviate = Weaviate()
    firestore = Firestore()

    # Get the messages field from the request
    data = json.loads(request.get_data())
    messages = data.get("messages")
    conversation = Conversation(messages)

    animus = Animus(firestore, weaviate, conversation)
    conversation, instructions, actions, memories = animus.main()

    # Convert the messages, instructions, actions, and memories to json
    response = {
        "messages": conversation.messages,
        "instructions": [instruction.to_dict() for instruction in instructions],
        "actions": actions,
        "memories": memories
    }
    # Return response
    return json.dumps(response)
