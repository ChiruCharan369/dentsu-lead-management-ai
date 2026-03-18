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


<<<<<<< HEAD
def safe_load_json(text: str):

    try:
        return json.loads(text)
    except Exception as e:
        print("JSON ERROR:", e)
        print("RAW:", text)
        return {}
=======
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
>>>>>>> b8874193d003bbf6ed15c49ad356c3a07c44ed94


def get_icp_data(company: str) -> ICPResponse:

    prompt = ICP_PROMPT.format(company=company)

    response = llm.invoke(prompt)

    text = response.content

    text = clean_json(text)

    data = safe_load_json(text)

    # replace None
    data = {k: (v if v is not None else "") for k, v in data.items()}

<<<<<<< HEAD
    return ICPResponse(**data)
=======
    # Calculate fitment
    data["ICPFitmentTest"] = calculate_fitment(data)

    return ICPResponse(**data)
>>>>>>> b8874193d003bbf6ed15c49ad356c3a07c44ed94
