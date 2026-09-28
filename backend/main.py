"""
LYRA - Phase 1 Backend (Ollama provider ke sath, updated)
Yeh file backend server hai. /chat endpoint ab providers.py ke through
AI se baat karta hai - abhi Ollama (local, free), kal koi aur provider bhi
ho sakta hai bina is file ko chhue.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from providers import get_provider

load_dotenv()

app = FastAPI(title="LYRA Backend - Phase 1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def health_check():
    return {"status": "LYRA backend is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message khaali nahi ho sakta")

    try:
        provider = get_provider()
        reply_text = provider.chat(request.message)
        return ChatResponse(reply=reply_text)

    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI se baat karte waqt error: {str(e)}")
