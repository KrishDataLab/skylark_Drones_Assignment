from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.agent.bi_agent import BIAgent
from backend.data.models import BIQueryResult

router = APIRouter()
agent = BIAgent()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat", response_model=BIQueryResult)
async def chat_endpoint(req: ChatRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query text cannot be empty.")
    
    result = await agent.process_query(req.query.strip())
    return result
