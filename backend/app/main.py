from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="AI Meeting Copilot API")

app.include_router(auth.router)

@app.get("/health")
def health():
    return {"status": "ok"}