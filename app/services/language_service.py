from app.prompts.detect_language_prompt import DETECT_LANGUAGE_PROMPT
from app.models.language_model import DetectLanguageResponse
from app.llm.llm_client import llm
from fastapi import HTTPException
import json
import re


def clean_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


def detect_language(data: dict) -> DetectLanguageResponse:
    prompt = DETECT_LANGUAGE_PROMPT.format(**data)

    detector = llm.bind(response_format={"type": "json_object"})

    resp = detector.invoke(prompt)
    raw = resp.content
    text = clean_json(raw)

    try:
        result = json.loads(text)
        return DetectLanguageResponse(**result)
    except json.JSONDecodeError:
        repair_prompt = f"""
Fix this into VALID JSON ONLY.
Do not add any extra text.
Make sure all quotes inside values are escaped.
JSON to fix:
{text}
"""
        resp2 = detector.invoke(repair_prompt)
        text2 = clean_json(resp2.content)

        try:
            result = json.loads(text2)
            return DetectLanguageResponse(**result)
        except Exception:
            print("RAW LLM OUTPUT:\n", raw)
            print("CLEANED OUTPUT:\n", text2)
            raise HTTPException(status_code=502, detail="Language detector returned invalid JSON")
