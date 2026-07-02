from pydantic import BaseModel


class DetectLanguageRequest(BaseModel):
    Comments: str = ""


class DetectLanguageResponse(BaseModel):
    Comments: str = ""
