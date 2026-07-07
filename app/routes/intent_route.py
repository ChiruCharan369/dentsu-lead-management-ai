from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.intent_service import classify_intent

router = APIRouter()


class IntentRequest(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    comment: Optional[str] = None


@router.post("/classify-intent")
async def classify_intent_api(request: IntentRequest):
    result = classify_intent(
        request.model_dump(exclude_none=True)
    )

    return {
        "result": result
    }