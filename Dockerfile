# 1. 베이스 이미지 (경량 Python)
FROM python:3.11-slim

# 2. 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. 작업 디렉토리 생성
WORKDIR /app

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. FastAPI 앱 소스 복사
COPY . .

# 6. Gunicorn + Uvicorn으로 실행 (생산 환경)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
