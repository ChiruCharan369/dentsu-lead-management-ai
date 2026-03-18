import json
import re

from app.prompts.icp_prompt import ICP_PROMPT
from app.models.icp_model import ICPResponse
from app.llm.llm_client import llm


def clean_json(text: str):
    import re

    # extract json block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    # remove markdown
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # fix missing quotes on keys
    text = re.sub(r'(\w+):', r'"\1":', text)

    # fix broken https cases
    text = text.replace('"https"://', '"https://')
    text = text.replace('""https://', '"https://')
    text = text.replace('"https//', '"https://')

    # fix url without quotes
    text = re.sub(
        r'"ICPLinkedInURL":\s*(https?://[^",]+)',
        r'"ICPLinkedInURL": "\1"',
        text,
    )

    return text.strip()


def safe_load_json(text: str):

    try:
        return json.loads(text)
    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW:", text)
        return {}


def get_icp_data(company: str) -> ICPResponse:

    prompt = ICP_PROMPT.format(company=company)

    response = llm.invoke(prompt)

    text = response.content

    text = clean_json(text)

    data = safe_load_json(text)

    # replace None
    data = {k: (v if v is not None else "") for k, v in data.items()}

    return ICPResponse(**data)
