from asyncio.log import logger
import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import text



# --- DB setup ---
DATABASE_URL = os.getenv(
    "DATABASE_URL_ASYNC", "postgresql+asyncpg://todo_huws_user:DJRA3oJSU35FeVeA7io6UlvezqjjZb5R@dpg-d2rrovp5pdvs73eckql0-a/todo_huws" 
)
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
