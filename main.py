from typing import Union

from fastapi import FastAPI
from summary.router import router as summary_router

app = FastAPI()
app.include_router(summary_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
