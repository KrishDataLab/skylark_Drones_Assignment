from fastapi import APIRouter
from backend.config.settings import settings
from backend.integrations.monday.client import MondayClient

router = APIRouter()

@router.get("/health")
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
