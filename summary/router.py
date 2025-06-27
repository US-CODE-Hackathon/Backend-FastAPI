from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from summary.service import get_summary

router = APIRouter()


class SummaryRequest(BaseModel):
    input: str


class SummaryResponse(BaseModel):
    output: str


@router.post("/summary", response_model=SummaryResponse)
def summary_endpoint(request: SummaryRequest):
    try:
        output = get_summary(request.input)
        return SummaryResponse(output=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
