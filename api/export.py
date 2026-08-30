import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fastapi import FastAPI
from backend.api.routes.export import generate_leadership_report

app = FastAPI()

@app.get("/")
@app.get("/api/export/leadership-update")
@app.get("/leadership-update")
async def get_leadership_report():
    return await generate_leadership_report()
