from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from summary.service import get_summary_detail, summarize_pattern
from sqlalchemy.orm import Session
from db import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class QnaItem(BaseModel):
    question: str
    answer: str


class SummaryDetailResponse(BaseModel):
    title: str
    sentiment: str
    summary: str


class PatternResponse(BaseModel):
    positive_ratio: float
    pattern_summary: str


@router.post("/summary", response_model=SummaryDetailResponse)
def summary_detail_endpoint(qna_list: List[QnaItem]):
    try:
        qna_dicts = [qna.dict() for qna in qna_list]
        result = get_summary_detail(qna_dicts)
        return SummaryDetailResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/analyze/{idx}", response_model=PatternResponse)
def analyze_summary(idx: int, db: Session = Depends(get_db)):
    return summarize_pattern(db, idx)
