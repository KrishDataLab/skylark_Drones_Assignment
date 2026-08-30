import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.agent.bi_agent import BIAgent

app = FastAPI()
agent = BIAgent()

class ChatRequest(BaseModel):
    query: str

@app.post("/")
@app.post("/api/chat")
async def process_chat(req: ChatRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    res = await agent.process_query(req.query.strip())
    return res.dict()
