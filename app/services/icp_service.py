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


def calculate_fitment(data: dict) -> str:
    weights = {
        "ICPIndustry": 20,
        "ICPEmployeesRange": 15,
        "ICPRevenueUSD": 20,
        "ICPFundingType": 5,
        "ICPFundingStage": 5,
        "ICPParentCompany": 5,
        "ICPLinkedInURL": 5,
        "ICPMarketingSignal": 15,
        "ICPFitStatus": 10,
    }

    total_score = 0
    for key, weight in weights.items():
        if data.get(key):
            total_score += weight

    return "ICP Fitment" if total_score >= 70 else "ICP Non Fitment"


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

    # Calculate fitment
    data["ICPFitmentTest"] = calculate_fitment(data)

    return ICPResponse(**data)