from pydantic import BaseModel

class AnalysisResponse(BaseModel):
    sector: str
    report: str
    timestamp: str
    sources_count: int


class Token(BaseModel):
    access_token: str
    token_type: str
