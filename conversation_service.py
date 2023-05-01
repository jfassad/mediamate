from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(temperature=0.7,
                 openai_api_key=OPENAI_API_KEY,
                 model_name="gpt-3.5-turbo",
                 verbose=True)

conversation = ConversationChain(
    llm=llm,
    verbose=True,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm)
)


class ConversationService:
    @staticmethod
    def handle_message(message):
        return conversation.predict(input=message)
