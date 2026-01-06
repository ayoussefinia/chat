from asyncio.log import logger
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text
import httpx
from fastapi.middleware.cors import CORSMiddleware

# --- Tunnel to my ollama server ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")  # e.g. https://your-tunnel.example.com
# --- DB setup ---
DATABASE_URL = os.environ["DATABASE_URL"].replace(
    "postgresql://", "postgresql+asyncpg://"
)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
logger.info(f"Using DATABASE_URL_ASYNC = {DATABASE_URL}")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# --- DB models ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

# --- Pydantic schema ---
class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

# --- FastAPI app ---
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    from datetime import datetime
    return {"item_id": item_id, "q": datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")}

@app.get("/users", response_model=List[UserOut])
async def get_users():
    async with SessionLocal() as session:
        result = await session.execute(text("SELECT id, email FROM users"))
        rows = result.fetchall()
        return [{"id": r.id, "email": r.email} for r in rows]

# --- Run server manually (for local dev) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# CORS (so your frontend can call FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR-FRONTEND.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    prompt: str

class ChatOut(BaseModel):
    response: str

@app.post("/chat", response_model=ChatOut)
async def chat(body: ChatIn):
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    if not ollama_base_url:
        return ChatOut(response="OLLAMA_BASE_URL not set on server.")

    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    payload = {"model": model, "prompt": body.prompt, "stream": False}

    async with httpx.AsyncClient(timeout=60.0) as client:
        r = await client.post(f"{ollama_base_url}/api/generate", json=payload)
        # if it fails, return text so we can see why
        if r.status_code >= 400:
            return ChatOut(response=f"Upstream error {r.status_code}: {r.text[:500]}")
        data = r.json()

    return ChatOut(response=data.get("response", ""))



@app.get("/debug/env")
async def debug_env():
    return {
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL"),
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL"),
        "DATABASE_URL_ASYNC_set": bool(os.getenv("DATABASE_URL_ASYNC")),
    }
