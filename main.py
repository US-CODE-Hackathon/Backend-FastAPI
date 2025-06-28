from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summary.router import router as summary_router
from db import SessionLocal, engine, Base
from stt_tts.router import router as stt_tts_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://us-hackathon-3db73.firebaseapp.com",
    "https://us-hackathon-3db73.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(summary_router)
app.include_router(stt_tts_router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
