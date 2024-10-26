"""
CRURAG
"""
import logging
import pickle
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from utilities import weaviate_utilities
from utilities.string_utilities import cleanup_translated_text

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def init_messages(redis):
    """

    :return:
    """
    system_personas = [persona for persona in redis.get_personas() if persona['type'] == 'SYSTEM']
    other_personas = [persona for persona in redis.get_personas() if persona['type'] != 'SYSTEM']
    system_message = ', '.join([persona['description'] for persona in system_personas])
    persona_messages = [persona_message(persona) for persona in other_personas]

    return [SystemMessage(content=system_message)] + persona_messages


def persona_message(persona):
    if persona['type'] == 'HUMAN':
        return HumanMessage(content=persona['description'])
    elif persona['type'] == "AI":
        return AIMessage(content=persona['description'])


class MessageManager:
    """
    Message Manager
    """

    def __init__(self, lang_chain, redis, weaviate_service):
        self.lang_chain = lang_chain
        self.redis = redis
        self.weaviate_service = weaviate_service
        self.locale = "am"

    async def process_message(self, chat_id, message):
        """

        :param chat_id:
        :param message:
        :return:
        """
        serialized_obj = self.redis.get_chat(chat_id)
        if serialized_obj is None:
            chat_messages = init_messages(self.redis)
        else:
            chat_messages = pickle.loads(serialized_obj)

        # logger.info('INIT Messages: %s', chat_messages)
        relevant_info = self.weaviate_service.search(message)
        relevant_message = weaviate_utilities.flatten_response(relevant_info)
        if relevant_message:
            chat_messages.append(
                AIMessage(content="Use this information " + relevant_message)
            )
        chat_messages.append(HumanMessage(content=message))
        resp = self.lang_chain.chat(chat_messages)
        chat_messages.append(AIMessage(content=resp))

        if len(chat_messages) > 50:
            self.redis.delete_chat(chat_id)
        else:
            self.redis.set_chat(chat_id, chat_messages)

        return resp

