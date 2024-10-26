"""
Bot interface
"""

import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from dotenv import load_dotenv
from message.message_manager import MessageManager
from services.openai.langchain_service import LangChainService
from services.redis.redis_service import RedisService
from services.weaviate.weaviate_service import WeaviateService

load_dotenv(override=True)

message_manager = MessageManager(LangChainService(), RedisService(), WeaviateService())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """

    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(
        "VerseWise: Your Bible companion for Scripture and theology, "
        "offering clear insights and references with a Protestant perspective. "
        "Respectful and reverent in all discussions."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """

    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(
        "VerseWise Help: VerseWise is your Bible companion for exploring Scripture "
        "and theology. Ask for insights, explanations, or references with a Protestant "
        "focus. Respectful and clear, VerseWise enriches your understanding of the Bible."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """

    :param update:
    :param context:
    :return:
    """
    await update.message.reply_text(
        await message_manager.process_message(
            update.message.from_user.id, update.message.text
        )
    )


def main():
    """

    :return:
    """
    app = ApplicationBuilder().token(os.environ.get("TELEGRAM_BOT_KEY")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()


if __name__ == "__main__":
    main()
