from asyncio import sleep
from collections import defaultdict
from io import BytesIO
from os import getenv
from typing import Iterable

from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure, get_file, upload_file
from google.generativeai.types import File, HarmBlockThreshold
from google.generativeai.types.retriever_types import State

load_dotenv()

WELCOME_MESSAGE_REQUEST = "Show a welcome message explaining who you are and what you can do."
NO_CONTENT_ERROR_MESSAGE = "Cannot respond without any information!"

API_KEY = getenv("GEMINI_API_KEY")
MODEL = getenv("GEMINI_MODEL", "gemini-1.5-flash")
SYSTEM_INSTRUCTION = getenv("GEMINI_SYSTEM_INSTRUCTION")

configure(api_key=API_KEY)
model = GenerativeModel(
    model_name=MODEL,
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=HarmBlockThreshold.BLOCK_NONE,
)
chats = defaultdict(model.start_chat)


async def initial_message() -> str | None:
    response = await model.generate_content_async(WELCOME_MESSAGE_REQUEST)
    return response.text


def reset_conversation(chat_id: int) -> None:
    chats.pop(chat_id, None)


async def next_message(chat_id: int, text: str, files: Iterable[tuple[BytesIO, str]]) -> str:
    content = [file for data in files if (file := await _prepare_file(*data))] + [text or ""]
    if not any(content):
        return NO_CONTENT_ERROR_MESSAGE
    return await _send_message(chat_id, content)


async def _prepare_file(data: BytesIO, mime_type: str) -> File | None:
    file = await _upload_file(data, mime_type)
    return file if file.state.value == State.STATE_ACTIVE else None


async def _upload_file(data: BytesIO, mime_type: str) -> File:
    file = upload_file(data, mime_type=mime_type)
    while file.state.value == State.STATE_PENDING_PROCESSING:
        await sleep(1)
        file = get_file(file.name)
    return file


async def _send_message(chat_id: int, content: list[str | File]) -> str:
    try:
        response = await chats[chat_id].send_message_async(content)
        return response.text
    except Exception as e:
        return str(e)
