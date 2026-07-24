from fastapi import APIRouter

from app.models.intent_model import IntentRequest, IntentResponse
from app.services.intent_service import classify_intent

router = APIRouter()


@router.post("/classify-intent", response_model=IntentResponse)
async def classify_intent_api(request: IntentRequest):
    return classify_intent(request.model_dump(exclude_none=True))
