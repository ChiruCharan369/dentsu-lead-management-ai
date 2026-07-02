from fastapi import APIRouter
from app.models.language_model import DetectLanguageRequest, DetectLanguageResponse
from app.services.language_service import detect_language

router = APIRouter()


@router.post("/detect_language", response_model=DetectLanguageResponse)
def detect(req: DetectLanguageRequest):
    data = req.dict()

    if data.get("Comments"):
        data["Comments"] = data["Comments"].replace("\r\n", "\n").replace("\r", "\n")

    return detect_language(data)
