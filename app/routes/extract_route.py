from fastapi import APIRouter

from app.models.extract_model import ExtractRequest
from app.services.extract_service import extract_fields

router = APIRouter()


@router.post("/extract-fields")
async def extract(request: ExtractRequest):

    result = await extract_fields(
        request.body_text
    )

    return result