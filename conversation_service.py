from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(temperature=0.7,
                 openai_api_key=OPENAI_API_KEY,
                 model_name="gpt-3.5-turbo",
                 verbose=True)


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
            del ConversationService.conversations[sender]
            return True
        return False
