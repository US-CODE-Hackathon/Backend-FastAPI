import requests
import os
from dotenv import load_dotenv

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
load_dotenv()


def get_gemini_summary(user_input: str, api_key: str = None) -> str:
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API 키가 필요합니다."
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_input}]}]}
    params = {"key": api_key}
    try:
        response = requests.post(
            GEMINI_API_URL, headers=headers, params=params, json=data, timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini API 호출 오류: {e}"
