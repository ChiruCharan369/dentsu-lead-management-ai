from typing import Optional

from pydantic import BaseModel


class IntentRequest(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    comment: Optional[str] = None


class IntentResponse(BaseModel):
    result: str = ""
    reason: str = ""
