from pydantic import BaseModel

class UpdateReportRequest(BaseModel):
    title: str