import os
import sys

# Ensure root directory is in sys.path when invoked as Vercel entrypoint
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config.settings import settings
from backend.api.routes import health, chat, export

app = FastAPI(
    title=settings.app_name,
    version=settings.version
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(export.router, prefix="/api")

# Mount frontend dist static files if built locally (Vercel Edge CDN handles static files natively)
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if not os.environ.get("VERCEL") and os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
