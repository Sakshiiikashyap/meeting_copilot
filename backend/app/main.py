from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, meetings

app = FastAPI(title="AI Meeting Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(meetings.router)

@app.get("/health")
def health():
    return {"status": "ok"}