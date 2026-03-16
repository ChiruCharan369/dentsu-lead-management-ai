import json
import re

from app.prompts.icp_prompt import ICP_PROMPT
from app.models.icp_model import ICPResponse
from app.llm.llm_client import llm


def clean_json(text: str) -> str:
    """
    Remove ```json ``` wrappers from LLM output
    """

    if text.startswith("```"):
        text = re.sub(r"```json", "", text)
        text = re.sub(r"```", "", text)

    return text.strip()


def get_icp_data(company: str) -> ICPResponse:

    prompt = ICP_PROMPT.format(company=company)

    response = llm.invoke(prompt)

    text = response.content

    text = clean_json(text)

    try:
        data = json.loads(text)
    except Exception:
        raise Exception(f"Invalid JSON from LLM: {text}")

    # Replace None values with empty strings
    data = {key: (value if value is not None else "") for key, value in data.items()}

    return ICPResponse(**data)