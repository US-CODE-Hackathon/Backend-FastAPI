from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from summary.service import get_summary_detail

router = APIRouter()


class QnaItem(BaseModel):
    question: str
    answer: str


class SummaryDetailResponse(BaseModel):
    title: str
    sentiment: str
    summary: str


@router.post("/summary", response_model=SummaryDetailResponse)
def summary_detail_endpoint(qna_list: List[QnaItem]):
    try:
        qna_dicts = [qna.dict() for qna in qna_list]
        result = get_summary_detail(qna_dicts)
        return SummaryDetailResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
