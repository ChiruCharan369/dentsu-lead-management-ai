from app.prompts.translator_prompt import TRANSLATOR_PROMPT
from app.models.translator_model import TranslatorResponse
from app.llm.llm_client import llm
from fastapi import HTTPException
import json
import re


def clean_json(text: str):
    # extract JSON object only
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


def translate_fields(data: dict) -> TranslatorResponse:
    prompt = TRANSLATOR_PROMPT.format(**data)

    # ✅ force json_object response format
    translator_llm = llm.bind(response_format={"type": "json_object"})

    resp = translator_llm.invoke(prompt)
    raw = resp.content
    text = clean_json(raw)

    try:
        result = json.loads(text)
        return TranslatorResponse(**result)
    except json.JSONDecodeError:
        # ✅ one repair attempt (model fixes its own broken JSON)
        repair_prompt = f"""
Fix this into VALID JSON ONLY.
Do not add any extra text.
Make sure all quotes inside values are escaped.
JSON to fix:
{text}
"""
        resp2 = translator_llm.invoke(repair_prompt)
        text2 = clean_json(resp2.content)

        try:
            result = json.loads(text2)
            return TranslatorResponse(**result)
        except Exception:
            # print for debugging
            print("RAW LLM OUTPUT:\n", raw)
            print("CLEANED OUTPUT:\n", text2)
            raise HTTPException(status_code=502, detail="Translator returned invalid JSON")