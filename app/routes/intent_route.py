from fastapi import APIRouter
from pydantic import BaseModel

from app.services.intent_service import classify_intent

router = APIRouter()


class IntentRequest(BaseModel):
    comment: str


@router.post("/classify-intent")
async def classify_intent_api(request: IntentRequest):

    result = classify_intent(
        request.comment
    )

    return {
        "result": result
    }