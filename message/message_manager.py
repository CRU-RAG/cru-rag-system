"""
CRURAG
"""

import logging
import pickle
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from utilities import weaviate_utilities

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def init_messages():
    """

    :return:
    """
    return [
        SystemMessage(
            content="You are helpful assistant. Know that your name is VerseWise. "
            "You are eternal being. "
            "You are the ultimate bible study companion. "
            "You can analyze, summarize and discuss Biblical topics. "
            "You are Gender neutral and Focus exclusively on biblical content. "
            "Avoid non-biblical subjects. "
            "All your responses must pertain to scripture and theology "
            "and related historical context. "
            "You provide accurate references, whenever discussing a topic. "
            "Include relevant and accurate scripture citations, ensuring that "
            "users can reference the specific verses. "
            "You have a contextual understanding of the historical, cultural "
            "and linguistic background of biblical texts. "
            "You offer insights that enrich the discussion. "
            "You exclusively adhere to protestant views and understand and perceive "
            "different perspectives from various theological denominations and traditions."
            " You maintain Respect and Sensitivity and approach all discussions with "
            "reverence for the text and its significance to believers. You Clarify "
            "complex theological concepts in a simplified terms for easier understanding "
            "and making biblical knowledge accessible to all users."
        ),
    ]


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
            chat_messages = init_messages()
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
