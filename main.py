from logging import INFO, basicConfig
from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

import chat

load_dotenv()

token = getenv("BOT_TOKEN")
start_message = "Hello! How may I assist you today?"

basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)


def main() -> None:
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    talk_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), talk)
    application.add_handler(talk_handler)
    reset_handler = CommandHandler("reset", reset)
    application.add_handler(reset_handler)

    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = chat.next_message(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat.reset()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Conversation restarted.")


if __name__ == "__main__":
    main()
