import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    app_name: str = "Skylark Drones Monday.com BI Agent"
    version: str = "1.0.0"
    environment: str = os.getenv("ENVIRONMENT", "development")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Monday.com Config
    monday_api_token: Optional[str] = os.getenv("MONDAY_API_TOKEN", "")
    monday_deals_board_id: Optional[str] = os.getenv("MONDAY_DEALS_BOARD_ID", "")
    monday_work_orders_board_id: Optional[str] = os.getenv("MONDAY_WORK_ORDERS_BOARD_ID", "")
    
    # LLM Config
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

settings = Settings()
