import json

from app.llm.llm_client import llm
from app.prompts.extract_prompt import EXTRACT_PROMPT

EXPECTED_FIELDS = [
    "Email",
    "FirstName",
    "LastName",
    "Company",
    "Campaign",
    "JobTitle",
    "Country",
    "Comments",
]


def _normalize_extracted_data(data):
    if not isinstance(data, dict):
        return {field: {"value": "", "type": "string"} for field in EXPECTED_FIELDS}

    extracted = data.get("extracted_data", {})
    if not isinstance(extracted, dict):
        extracted = {}

    normalized = {}
    for field in EXPECTED_FIELDS:
        field_data = extracted.get(field, {})
        if isinstance(field_data, dict):
            value = field_data.get("value", "")
            if value is None:
                value = ""
            normalized[field] = {
                "value": str(value),
                "type": field_data.get("type", "string"),
            }
        else:
            normalized[field] = {"value": "", "type": "string"}

    return {"extracted_data": normalized}


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
        parsed = json.loads(content)
        return _normalize_extracted_data(parsed)

    except Exception:
        return {
            "error": "Invalid JSON returned by LLM",
            "raw_response": content,
            "extracted_data": {
                field: {"value": "", "type": "string"}
                for field in EXPECTED_FIELDS
            },
        }