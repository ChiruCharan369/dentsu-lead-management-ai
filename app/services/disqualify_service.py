from app.prompts.disqualify_prompt import DISQUALIFY_PROMPT
from app.models.disqualify_model import DisqualifyResponse
from app.llm.llm_client import llm
from fastapi import HTTPException
import re


def _clean_reason(text: str) -> str:
    if not text:
        return ""
    # take first non-empty line
    for line in text.splitlines():
        line = line.strip()
        if line:
            # remove surrounding quotes and trailing punctuation
            line = line.strip(' "\'')
            line = re.sub(r"[\.!?,;:]+$", "", line)
            return line
    return ""


def get_disqualification_reason(data: dict) -> DisqualifyResponse:
    prompt = DISQUALIFY_PROMPT.format(Comments=data.get("Comments", ""))

    resp = llm.invoke(prompt)
    raw = resp.content

    reason = _clean_reason(raw)

    if reason:
        return DisqualifyResponse(reason=reason)

    # repair attempt
    repair_prompt = f"Return ONLY a short disqualification reason (2-5 words) with no punctuation.\nInput:\n{data.get('Comments', '')}\n"
    resp2 = llm.invoke(repair_prompt)
    reason2 = _clean_reason(resp2.content)

    if reason2:
        return DisqualifyResponse(reason=reason2)

    print("RAW LLM OUTPUT:\n", raw)
    print("REPAIR OUTPUT:\n", resp2.content)
    raise HTTPException(status_code=502, detail="Failed to obtain disqualification reason")
