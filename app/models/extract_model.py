from pydantic import BaseModel


class ExtractRequest(BaseModel):
    body_text: str