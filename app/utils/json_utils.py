import json
import re


def clean_json_text(text: str) -> str:
    if not isinstance(text, str):
        return str(text)

    # Remove code fences and markdown artifacts
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)
    # Find first and last JSON object boundaries
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start:end+1]

    return text.strip()


def parse_json_text(text: str):
    try:
        return json.loads(clean_json_text(text))
    except json.JSONDecodeError:
        # try to repair common JSON issues
        repaired = re.sub(r"(\w+)\s*:\s*", r'"\1": ', text)
        repaired = repaired.replace("'", '"')
        try:
            return json.loads(clean_json_text(repaired))
        except Exception:
            raise
