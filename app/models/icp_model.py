from pydantic import BaseModel


class ICPRequest(BaseModel):
    company: str = ""
    email: str = ""


class ICPResponse(BaseModel):
    company: str = ""
    email: str = ""
    
    ICPIndustry: str = ""
    ICPEmployeesRange: str = ""
    ICPRevenueUSD: str = ""
    ICPFundingType: str = ""
    ICPFundingStage: str = ""
    ICPFUndingAmount: str = ""
    ICPParentCompany: str = ""
    ICPLinkedInURL: str = ""
    ICPMarketingSignal: str = ""
    ICPFitStatus: str = ""
    ICPFitmentTest: str = ""