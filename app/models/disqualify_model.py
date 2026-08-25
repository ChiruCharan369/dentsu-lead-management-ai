from pydantic import BaseModel


class DisqualifyRequest(BaseModel):
    Comments: str = ""


class DisqualifyResponse(BaseModel):
    reason: str = ""
