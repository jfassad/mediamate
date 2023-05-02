# This file defines a ConversationService class that provides functionality for handling messages and maintaining conversations
# between a user and a chatbot using the LangChain library, the ChatOpenAI model, and the ConversationChain class.

import logging

from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

llm = ChatOpenAI(temperature=0.7,
                 openai_api_key=OPENAI_API_KEY,
                 model_name="gpt-3.5-turbo")


def create_conversation_chain():
    return ConversationChain(
        llm=llm,
        verbose=True,
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=ConversationEntityMemory(llm=llm)
    )


class ConversationService:
    conversations = dict()

    @staticmethod
    def handle_message(sender, message):
        if message.strip().lower() == "clear context":
            ConversationService.remove_conversation(sender)
            return "Context cleared."

        if sender not in ConversationService.conversations:
            ConversationService.conversations[sender] = create_conversation_chain()

        conversation = ConversationService.conversations[sender]
        return conversation.predict(input=message)

    @staticmethod
    def remove_conversation(sender):
        if sender in ConversationService.conversations:
            conversation = ConversationService.conversations[sender]
            conversation.memory.clear()
            del ConversationService.conversations[sender]
            return True
        return False
