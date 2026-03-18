from pydantic import BaseModel


class ICPRequest(BaseModel):
    company: str


class ICPResponse(BaseModel):
    ICPIndustry: str = ""
    ICPEmployeesRange: str = ""
    ICPRevenueUSD: str = ""
    ICPFundingType: str = ""
    ICPFundingStage: str = ""
    ICPParentCompany: str = ""  # Default to an empty string
    ICPLinkedInURL: str = ""
    ICPMarketingSignal: str = ""
    ICPFitStatus: str = ""
    ICPFitmentTest: str = "" 
