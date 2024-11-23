from os import getenv

from dotenv import load_dotenv
from google.ai.generativelanguage_v1 import Content
from google.generativeai import GenerativeModel
from google.generativeai.types import ContentDict, HarmBlockThreshold

NO_IMAGE_RESPONSE = "NO_IMAGE_REQUESTED"
SYSTEM_INSTRUCTION = (
    f"You are a AI assistant tasked with identifying user requests for image generation. "
    f"Analyze the provided conversation history. Look for keywords, phrases, and the overall "
    f"context to determine if the user's last message requests an image. Consider phrases like "
    f"'draw', 'paint', 'create an image of', 'visualize', 'generate an image', etc. "
    f"If an image is requested, craft a detailed and descriptive image generation prompt suitable "
    f"for an image generation model. This prompt should include all relevant details from the "
    f"user's request, but focus on accurately reflecting user's vision. "
    f"Prioritize accuracy over generating a prompt when there is ambiguity. "
    f"If no image generation is requested, respond with '{NO_IMAGE_RESPONSE}'."
)

load_dotenv()

API_KEY = getenv("GEMINI_API_KEY")
MODEL = getenv("GEMINI_MODEL", "gemini-1.5-flash")
model = GenerativeModel(
    model_name=MODEL,
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings=HarmBlockThreshold.BLOCK_NONE,
)


async def requested_image_prompt(prompt: str, chat_history: list[Content]) -> str | None:
    if not prompt:
        return None
    full_history = chat_history + [ContentDict(role="user", parts=[prompt])]
    response = await model.generate_content_async(full_history)
    return None if NO_IMAGE_RESPONSE in response.text else response.text
