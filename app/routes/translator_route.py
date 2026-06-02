from fastapi import APIRouter
from app.models.translator_model import TranslatorRequest, TranslatorResponse
from app.services.translator_service import translate_fields

router = APIRouter()


# @router.post("/translator", response_model=TranslatorResponse)
# def translate(req: TranslatorRequest):

#     return translate_fields(req.dict())

@router.post("/translator", response_model=TranslatorResponse)
def translate(req: TranslatorRequest):
    data = req.dict()

    if data["Comments"]:
        data["Comments"] = data["Comments"].replace("\r\n", "\n").replace("\r", "\n")

    return translate_fields(data)
