import json
import re
from summary.adapter import get_gemini_summary
from typing import List, Dict
from summary.model import EmotionalReport
from sqlalchemy.orm import Session


def get_summary_detail(qna_list: List[Dict[str, str]]) -> Dict[str, str]:
    # 1) Q&A를 JSON 배열 문자열로 만들기
    convo_json = json.dumps(qna_list, ensure_ascii=False, indent=2)

    # 2) 프롬프트 생성 (f‑string 중괄호는 이미 이스케이프 되어 있다고 가정)
    prompt = f"""
아래는 어르신과의 오늘 하루 대화 기록입니다.
각 항목은 question/answer로 구성된 JSON 배열입니다.

이 데이터를 바탕으로,
1) 하루를 대표하는 제목(title, 30자 이내)
2) 전체 감정 흐름(sentiment: '긍정'/'부정'/'보통')
3) 2~3문장으로 자연스럽게 작성된 summary

위 세 가지를 JSON 형태로 하나만 반환해주세요.

입력 데이터:
{convo_json}
"""

    # 3) Gemini 호출
    gemini_response = get_gemini_summary(prompt)

    # 4) 응답에서 JSON 부분만 추출한 뒤 파싱
    #   - ```json\n{...}\n``` 형태
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", gemini_response, re.DOTALL)
    json_str = m.group(1) if m else gemini_response

    #   - 혹은 중괄호{} 블록만 뽑아내기
    if not m:
        m2 = re.search(r"(\{.*\})", gemini_response, re.DOTALL)
        if m2:
            json_str = m2.group(1)

    # 5) 파싱 및 반환
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # 최종 fallback: 빈값 반환
        print("Gemini 응답 파싱 실패:", gemini_response)
        return {"title": "", "sentiment": "보통", "summary": ""}


def summarize_pattern(db: Session, idx: int):
    entries = get_recent_entries(db, idx)
    ratio = calculate_positive_ratio(entries)
    percent_str = f"{int(ratio * 100)}%"
    merged = "\n".join([f"{e.title}\n{e.summary}" for e in entries])
    analysis = call_gemini_api(merged, idx, percent_str)
    return {"positive_ratio": ratio, "pattern_summary": analysis}


# 최근 N개 emotional_report 데이터 가져오기
def get_recent_entries(db: Session, count: int):
    return (
        db.query(EmotionalReport)
        .order_by(EmotionalReport.created_at.desc())
        .limit(count)
        .all()
    )


# 긍정 비율 계산
def calculate_positive_ratio(entries):
    if not entries:
        return 0.0
    positive_count = sum(1 for e in entries if e.sentiment == "긍정")
    return positive_count / len(entries)


# Gemini API로 패턴 분석 요청
def call_gemini_api(merged_text: str, count: int, percent_str: str) -> str:
    prompt = f"""
아래는 최근 {count}일간의 감정 리포트 제목과 요약입니다. 이 데이터를 바탕으로 전문 심리상담가가 작성하는 정서 진단서 형식으로, 다음 항목을 포함해 자연스러운 한글 문장으로만 상세하게 분석해 주세요.

1. 전체 기간의 긍정 감정 비율: {percent_str}
2. 정서 상태의 변화 및 주요 특징
3. 반복적으로 나타나는 감정 패턴
4. 주목할 만한 변화나 이슈
5. 전반적인 심리 상태에 대한 전문가적 평가 및 조언

총 응답 글자수는 40글자를 넘지 말아주세요.
※ 마크다운, 특수문자, 불필요한 기호 없이 자연스러운 한글 문장으로만 작성해 주세요.

입력 데이터:
{merged_text}

위 항목을 포함해 5~7문장 내외로, 실제 진단서처럼 전문적이고 신뢰감 있게 작성해 주세요.
"""
    return get_gemini_summary(prompt)
