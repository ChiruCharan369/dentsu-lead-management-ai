from fastapi import APIRouter
from app.models.disqualify_model import DisqualifyRequest, DisqualifyResponse
from app.services.disqualify_service import get_disqualification_reason

router = APIRouter()


@router.post("/disqualify-reason", response_model=DisqualifyResponse)
def disqualify(req: DisqualifyRequest):
    data = req.dict()

    if data.get("Comments"):
        data["Comments"] = data["Comments"].replace("\r\n", "\n").replace("\r", "\n")

    return get_disqualification_reason(data)
