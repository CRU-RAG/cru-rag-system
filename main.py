"""
CRURAG
"""

import os
import asyncio
from urllib.parse import urlparse, parse_qs
import websockets
from dotenv import load_dotenv
from message.message_manager import MessageManager
from services.openai.langchain_service import LangChainService
from services.redis.redis_service import RedisService
from services.weaviate.weaviate_service import WeaviateService

load_dotenv(override=True)

message_manager = MessageManager(
    LangChainService(), RedisService(), WeaviateService()
)


async def echo(websocket, path):
    """
    echo
    :param websocket:
    :param path:
    :return:
    """
    chat_id = parse_qs(urlparse(path).query).get("id", [None])[0]
    async for message in websocket:
        await websocket.send(await message_manager.process_message(chat_id, message))


async def main():
    """
    Main
    :return:
    """
    async with websockets.serve(echo, "0.0.0.0", os.environ.get("APP_PORT")):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
