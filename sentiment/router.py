from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentiment.adapter import analyze_sentiment

router = APIRouter()


class SentimentRequest(BaseModel):
    input: str


class SentimentResponse(BaseModel):
    label: str  # 긍정/부정/보통
    score: float
    magnitude: float
    language: str


def score_to_label(score: float) -> str:
    if score >= 0.3:
        return "긍정"
    elif score <= -0.3:
        return "부정"
    else:
        return "보통"


@router.post("/sentiment", response_model=SentimentResponse)
def sentiment_endpoint(request: SentimentRequest):
    try:
        result = analyze_sentiment(request.input, language_code="ko")
        label = score_to_label(result["score"])
        return SentimentResponse(
            label=label,
            score=result["score"],
            magnitude=result["magnitude"],
            language=result["language"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
