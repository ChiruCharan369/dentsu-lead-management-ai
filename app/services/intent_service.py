import re
from typing import Any, Mapping

from app.llm.llm_client import llm
from app.prompts.intent_prompt import INTENT_PROMPT


def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload.strip()

    if isinstance(payload, Mapping):
        comment = (
            payload.get("Comments")
            or payload.get("comments")
            or payload.get("comment")
            or payload.get("Comment")
            or payload.get("message")
            or payload.get("Message")
            or payload.get("body_text")
            or payload.get("BodyText")
            or ""
        )
        first_name = payload.get("FirstName") or payload.get("firstName") or payload.get("first_name") or ""
        last_name = payload.get("LastName") or payload.get("lastName") or payload.get("last_name") or ""

        if isinstance(comment, str) and comment.strip():
            return comment.strip()

        parts = [str(part).strip() for part in (first_name, last_name, comment) if str(part).strip()]
        return " ".join(parts).strip()

    return str(payload or "").strip()


def _parse_revenue(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().lower().replace("$", "").replace(",", "")
    if not text:
        return None

    match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(k|m|b|thousand|million|billion)?", text)
    if not match:
        return None

    number = float(match.group(1))
    suffix = (match.group(2) or "").strip()

    if suffix in {"k", "thousand"}:
        return number * 1000
    if suffix in {"m", "million"}:
        return number * 1_000_000
    if suffix in {"b", "billion"}:
        return number * 1_000_000_000

    return number


def _is_service_provider_outreach(text: str) -> bool:
    if not text:
        return False

    lowered = text.lower()
    service_keywords = re.search(r"\b(seo|backlink|backlinks|guest post|guest posts|media kit|link insertion|link building|placement|services|service|agency|vendor|consulting|website|traffic|ranking)\b", lowered)
    outreach_patterns = re.search(r"\b(we offer|we provide|i offer|i can help|we can help|help your|help your agency|our services|our service|service provider|vendor outreach)\b", lowered)

    return bool(service_keywords and outreach_patterns)


def _is_placeholder_or_gibberish(payload: Any) -> bool:
    text = _extract_text(payload).strip()
    if not text:
        return False

    normalized = re.sub(r"[^a-z0-9]+", "", text.lower())
    placeholder_values = {"string", "test", "sample", "example", "none", "null", "na", "n/a", "hello", "hi", "hey", "hola"}

    if normalized in placeholder_values:
        return True

    if len(normalized) <= 3 and not any(vowel in normalized for vowel in "aeiou"):
        return True

    if not any(vowel in normalized for vowel in "aeiou"):
        return True

    if len(set(normalized)) <= 3 and len(normalized) <= 8:
        return True

    words = re.findall(r"[a-z]{2,}", text.lower())
    if len(words) >= 3 and all(len(word) <= 4 for word in words):
        common_words = {"need", "want", "looking", "help", "hire", "agency", "marketing", "seo", "digital", "service", "services", "partner", "collaboration", "project", "campaign", "brand", "website", "advertising", "media", "social", "growth", "sales", "lead", "consulting", "support"}
        if not any(word in common_words for word in words):
            return True

    return False


def _has_no_comment_with_high_revenue(payload: Any, text: str) -> bool:
    if text:
        return False

    if isinstance(payload, Mapping):
        revenue = (
            payload.get("ICPRevenueUSD")
            or payload.get("Revenue")
            or payload.get("annual_revenue")
            or payload.get("AnnualRevenue")
            or payload.get("revenue")
            or ""
        )
        parsed = _parse_revenue(revenue)
        if parsed is not None and parsed > 1_000_000:
            return True

    return False


def _is_gibberish_name(name: Any) -> bool:
    if not isinstance(name, str) or not name.strip():
        return False

    value = name.strip()
    lower = value.lower()

    placeholder_name_pattern = re.compile(r"^(#?sym[:_\-]?)?(first(name)?|last(name)?|name|firstname|lastname)$", re.I)
    if placeholder_name_pattern.match(lower):
        return True

    if re.search(r"\d", value):
        return True

    letters_only = re.sub(r"[^a-z]+", "", lower)
    if not letters_only:
        return True

    if len(letters_only) <= 2:
        return False

    vowel_count = sum(1 for c in letters_only if c in "aeiou")
    if vowel_count == 0:
        return True

    if len(letters_only) >= 5 and vowel_count / len(letters_only) < 0.25:
        return True

    if len(value) >= 10 and value.isalnum() and any(c.isupper() for c in value) and any(c.islower() for c in value):
        return True

    if re.search(r"[^a-zA-Z\s]", value):
        non_alpha_chars = re.findall(r"[^a-zA-Z\s]", value)
        if len(non_alpha_chars) / len(value) > 0.25:
            return True

    if re.search(r"[bcdfghjklmnpqrstvwxyz]{4,}", letters_only):
        return True

    return False


def _names_are_gibberish(payload: Any) -> bool:
    if not isinstance(payload, Mapping):
        return False

    first_name = payload.get("FirstName") or payload.get("firstName") or payload.get("first_name") or ""
    last_name = payload.get("LastName") or payload.get("lastName") or payload.get("last_name") or ""

    return _is_gibberish_name(first_name) or _is_gibberish_name(last_name)


def classify_intent(payload: Any) -> str:
    text = _extract_text(payload)

    if _is_service_provider_outreach(text):
        return "non qualified"

    if _names_are_gibberish(payload):
        return "non qualified"

    if _has_no_comment_with_high_revenue(payload, text):
        return "qualified"

    if _is_placeholder_or_gibberish(payload):
        return "non qualified"

    # Provide optional first/last name fields when formatting the prompt
    first_name = ""
    last_name = ""
    if isinstance(payload, Mapping):
        first_name = payload.get("FirstName") or payload.get("firstName") or payload.get("first_name") or ""
        last_name = payload.get("LastName") or payload.get("lastName") or payload.get("last_name") or ""

    prompt = INTENT_PROMPT.format(
        FirstName=first_name,
        LastName=last_name,
        comment=text,
    )

    response = llm.invoke(prompt)

    result = response.content.strip().lower()

    if "qualified" == result:
        return "qualified"

    return "non qualified"