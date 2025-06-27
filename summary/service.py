import json
import re
from summary.adapter import get_gemini_summary
from typing import List, Dict

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
