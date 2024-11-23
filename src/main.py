from io import BytesIO
from os import getenv
from pathlib import Path
from textwrap import wrap

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.events import NewMessage, StopPropagation
from telethon.tl.patched import Message

from ai.chat import chat_history, initial_message, next_message, reset_conversation
from ai.images import generate_image
from ai.response_type import requested_image_prompt

load_dotenv()
SESSION = getenv("SESSION", "gemini")
API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
ALLOWED_USERS = getenv("ALLOWED_USERNAMES", "").split()
MAX_MESSAGE_LENGTH = int(getenv("MAX_MESSAGE_LENGTH", 4096))

bot = TelegramClient(Path(SESSION), API_ID, API_HASH).start(bot_token=BOT_TOKEN)


def main() -> None:
    bot.run_until_disconnected()


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True, pattern="/start"))
async def start(event: NewMessage.Event) -> None:
    async with bot.action(event.chat_id, "typing"):
        message = await initial_message()
        await send(event, message)
    raise StopPropagation


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True, pattern="/restart"))
async def restart(event: NewMessage.Event) -> None:
    async with bot.action(event.chat_id, "typing"):
        reset_conversation(event.chat_id)
        await send(event, "Conversation restarted.")
    raise StopPropagation


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True))
async def talk(event: NewMessage.Event) -> None:
    message = event.message
    prompt = message.text
    async with bot.action(event.chat_id, "typing"):
        if not (image_prompt := await requested_image_prompt(prompt, chat_history(event.chat_id))):
            files = await get_file(message)
            response = await next_message(event.chat_id, prompt, files)
            await send(event, response)
            return
        await send(event, "Generating image...")
    async with bot.action(event.chat_id, "photo"):
        image = await generate_image(image_prompt)
        # Send image


async def get_file(message: Message) -> list[tuple[BytesIO, str]]:
    if not (file := message.file):
        return []
    media = await message.download_media(file=bytes)
    mime_type = file.mime_type
    return [(BytesIO(media), mime_type)]


async def send(event: NewMessage.Event, text: str) -> None:
    parts = wrap(
        text.strip(),
        MAX_MESSAGE_LENGTH,
        tabsize=4,
        break_long_words=False,
        replace_whitespace=False,
        break_on_hyphens=False,
        drop_whitespace=False,
    )
    for partial in parts:
        await event.respond(partial.strip())


if __name__ == "__main__":
    main()
