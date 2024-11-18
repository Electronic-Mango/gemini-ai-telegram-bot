from io import BytesIO
from logging import INFO, basicConfig
from mimetypes import guess_type
from os import getenv
from textwrap import wrap
from typing import Sequence

from dotenv import load_dotenv
from telegram import Message, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from telegram.ext.filters import COMMAND

from chat import initial_message, next_message, reset_conversation
from user_filer import user_filter

(INPUT_PROMPT_STATE,) = range(1)


def main() -> None:
    load_dotenv()
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)
    bot = ApplicationBuilder().token(getenv("BOT_TOKEN")).build()
    bot.add_handler(CommandHandler("start", start, user_filter))
    bot.add_handler(CommandHandler("restart", restart, user_filter))
    bot.add_handler(MessageHandler(user_filter & ~COMMAND, talk))
    bot.run_polling()


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = await initial_message()
    await send(message, update)


async def restart(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reset_conversation(update.effective_chat.id)
    await send("Conversation restarted.", update)


async def talk(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    text = message.text or message.caption or ""
    file_data = await get_file(ctx, message)
    response = await next_message(update.effective_chat.id, text, file_data)
    await send(response, update)


async def get_file(ctx: ContextTypes.DEFAULT_TYPE, message: Message) -> list[tuple[BytesIO, str]]:
    if not (attachment := message.effective_attachment):
        return []
    if isinstance(attachment, Sequence):
        attachment = max(attachment, key=lambda p: p.file_size or 0)
    file = await ctx.bot.get_file(attachment)
    file_array = await file.download_as_bytearray()
    mime_type = getattr(attachment, "mime_type", None) or guess_type(file.file_path)[0]
    return [(BytesIO(file_array), mime_type)]


async def send(message: str, update: Update) -> None:
    max_length = int(getenv("MAX_MESSAGE_LENGTH", 4096))
    if len(message) <= max_length:
        await update.message.reply_text(message.strip())
        return
    parts = wrap(
        message,
        max_length,
        tabsize=4,
        break_long_words=False,
        replace_whitespace=False,
        break_on_hyphens=False,
        drop_whitespace=False,
    )
    for partial in parts:
        await update.message.reply_text(partial.strip())


if __name__ == "__main__":
    main()
