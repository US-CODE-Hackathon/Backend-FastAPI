from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from google.cloud import speech, texttospeech
import io
import os

router = APIRouter()


# STT 엔드포인트
@router.post("/stt")
async def speech_to_text(file: UploadFile = File(...)):
    filename = file.filename.lower()
    if filename.endswith(".wav"):
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
        sample_rate = 16000  # 실제 wav 파일의 샘플레이트로 맞추세요
    elif filename.endswith(".mp3"):
        encoding = speech.RecognitionConfig.AudioEncoding.MP3
        sample_rate = 44100  # 실제 mp3 파일의 샘플레이트로 맞추세요
    else:
        return {"text": "지원하지 않는 파일 포맷입니다. wav 또는 mp3만 업로드하세요."}

    client = speech.SpeechClient()
    audio_content = await file.read()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        language_code="ko-KR",
    )
    response = client.recognize(config=config, audio=audio)
    transcript = " ".join(
        [result.alternatives[0].transcript for result in response.results]
    )
    return {"text": transcript}


# TTS 엔드포인트
@router.post("/tts")
async def text_to_speech(text: str = Form(...)):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Chirp3-HD-Aoede",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mp3")
