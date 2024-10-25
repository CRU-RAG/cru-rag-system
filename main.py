"""
Lucy
"""

import os
import asyncio
from urllib.parse import urlparse, parse_qs
import websockets
from dotenv import load_dotenv

load_dotenv(override=True)


async def echo(websocket, path):
    """
    echo
    :param websocket:
    :param path:
    :return:
    """
    chat_id = parse_qs(urlparse(path).query).get("id", [None])[0]
    async for message in websocket:
        await websocket.send(message + chat_id)


async def main():
    """
    Main
    :return:
    """
    async with websockets.serve(echo, "0.0.0.0", os.environ.get("APP_PORT")):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
