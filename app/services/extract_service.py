import json

from app.llm.llm_client import llm
from app.prompts.extract_prompt import EXTRACT_PROMPT


async def extract_fields(body_text: str):

    prompt = EXTRACT_PROMPT.replace(
        "{body_text}",
        body_text
    )

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()

    try:
        return json.loads(content)

    except Exception:
        return {
            "error": "Invalid JSON returned by LLM",
            "raw_response": content
        }