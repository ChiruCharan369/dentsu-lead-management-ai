from fastapi import APIRouter
from app.models.icp_model import ICPRequest, ICPResponse
from app.services.icp_service import get_icp_data

router = APIRouter()


@router.post("/icp", response_model=ICPResponse)
def icp_check(req: ICPRequest):

    result = get_icp_data(
        company=req.company,
        email=req.email,
    )

    return result