from io import BytesIO
from os import getenv

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.events import NewMessage, StopPropagation
from telethon.tl.patched import Message

from chat import initial_message, next_message, reset_conversation

load_dotenv()
SESSION = "Gemini AI"
API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
ALLOWED_USERS = getenv("ALLOWED_USERNAMES", "").split()

bot = TelegramClient(SESSION, API_ID, API_HASH).start(bot_token=BOT_TOKEN)


def main() -> None:
    bot.run_until_disconnected()


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True, pattern="/start"))
async def start(event: NewMessage.Event) -> None:
    async with bot.action(event.chat_id, "typing"):
        message = await initial_message()
        await event.respond(message)
    raise StopPropagation


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True, pattern="/restart"))
async def restart(event: NewMessage.Event) -> None:
    async with bot.action(event.chat_id, "typing"):
        reset_conversation(event.chat_id)
        await event.respond("Conversation restarted.")
    raise StopPropagation


@bot.on(NewMessage(from_users=ALLOWED_USERS, incoming=True))
async def talk(event: NewMessage.Event) -> None:
    async with bot.action(event.chat_id, "typing"):
        message = event.message
        prompt = message.text
        files = await get_file(message)
        response = await next_message(event.chat_id, prompt, files)
        await event.respond(response)


async def get_file(message: Message) -> list[tuple[BytesIO, str]]:
    if not (file := message.file):
        return []
    media = await message.download_media(file=bytes)
    mime_type = file.mime_type
    return [(BytesIO(media), mime_type)]


if __name__ == "__main__":
    main()
