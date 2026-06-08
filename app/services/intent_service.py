from app.llm.llm_client import llm
from app.prompts.intent_prompt import INTENT_PROMPT


def classify_intent(comment: str) -> str:

    prompt = INTENT_PROMPT.format(
        comment=comment
    )

    response = llm.invoke(prompt)

    result = response.content.strip().lower()

    if "qualified" == result:
        return "qualified"

    return "non qualified"