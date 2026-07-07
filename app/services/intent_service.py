import re
from typing import Any, Mapping

from app.llm.llm_client import llm
from app.prompts.intent_prompt import INTENT_PROMPT


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()

    if isinstance(payload, Mapping):
        comment = payload.get("comment") or payload.get("Comment") or payload.get("message") or payload.get("Message") or ""
        first_name = payload.get("FirstName") or payload.get("firstName") or payload.get("first_name") or ""
        last_name = payload.get("LastName") or payload.get("lastName") or payload.get("last_name") or ""

        if isinstance(comment, str) and comment.strip():
            return comment.strip()

        parts = [str(part).strip() for part in (first_name, last_name, comment) if str(part).strip()]
        return " ".join(parts).strip()

    return str(payload or "").strip()


def _is_placeholder_or_gibberish(payload: Any) -> bool:
    text = _extract_text(payload).strip()
    if not text:
        return True

    normalized = re.sub(r"[^a-z0-9]+", "", text.lower())
    placeholder_values = {"string", "test", "sample", "example", "none", "null", "na", "n/a", "hello", "hi", "hey", "hola"}

    if normalized in placeholder_values:
        return True

    if len(normalized) <= 3 and not any(vowel in normalized for vowel in "aeiou"):
        return True

    return False


def classify_intent(payload: Any) -> str:
    if _is_placeholder_or_gibberish(payload):
        return "non qualified"

    prompt = INTENT_PROMPT.format(
        comment=_extract_text(payload)
    )

    response = llm.invoke(prompt)

    result = response.content.strip().lower()

    if "qualified" == result:
        return "qualified"

    return "non qualified"