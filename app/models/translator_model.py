from pydantic import BaseModel


class TranslatorRequest(BaseModel):
    FirstName: str = ""
    LastName: str = ""
    company: str = ""
    JobTitle: str = ""
    Comments: str = ""


class TranslatorResponse(BaseModel):
    FirstNameEnglish: str = ""
    LastNameEnglish: str = ""
    companyEnglish: str = ""
    JobTitleEnglish: str = ""
    CommentsEnglish: str = ""
