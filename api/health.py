import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI
from mangum import Mangum
from backend.config.settings import settings
from backend.integrations.monday.client import MondayClient

app = FastAPI()

@app.get("/")
@app.get("/api/health")
async def health_check():
    monday_client = MondayClient()
    is_live = bool(settings.monday_api_token and settings.monday_deals_board_id and settings.monday_work_orders_board_id)
    return {
        "status": "online",
        "app": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "monday_integration": {
            "mode": "live_graphql" if is_live else "local_seed_fallback",
            "is_configured": is_live
        }
    }

handler = Mangum(app)
