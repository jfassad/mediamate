import logging

from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.chat_models import ChatOpenAI
from config import OPENAI_API_KEY

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents import load_tools


logger = logging.getLogger(__name__)

llm = ChatOpenAI(temperature=0.0,
                 openai_api_key=OPENAI_API_KEY,
                 model_name="gpt-3.5-turbo")

tools = load_tools(["google-serper"], llm=llm)

conversations = {}


def _create_conversation_chain():
    return ConversationChain(
        llm=llm,
        memory=ConversationTokenBufferMemory(llm=llm, max_token_limit=4000),
        verbose=True
    )


def _create_conversation_agent():
    return initialize_agent(
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        memory=ConversationTokenBufferMemory(llm=llm, memory_key="chat_history", max_token_limit=4000),
        max_iterations=5,
        handle_parsing_errors=False,
        verbose=True)


def _remove_conversation(sender):
    logger.debug(f"Removing conversation for {sender}")
    if sender in conversations:
        conversation = conversations[sender]
        conversation.memory.clear()
        del conversations[sender]
        return True
    return False


def handle_conversation(sender, message):
    message_lower = message.strip().lower()

    if message_lower in ["clear context", "start agent conversation", "start chain conversation"]:
        _remove_conversation(sender)

        if message_lower == "start agent conversation":
            conversations[sender] = _create_conversation_agent()
        elif message_lower == "start chain conversation":
            conversations[sender] = _create_conversation_chain()

        return "Ok"

    if sender not in conversations:
        logger.debug(f"Creating new conversation for {sender}")
        conversations[sender] = _create_conversation_chain()

    conversation = conversations[sender]

    if isinstance(conversation, ConversationChain):
        response = conversation.predict(input=message)
    else:
        response = conversation.run(input=message)

    return response

