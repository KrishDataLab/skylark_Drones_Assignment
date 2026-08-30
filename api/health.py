from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
@app.get("/api/health")
def health():
    return {"status": "online", "app": "Skylark Drones Monday.com BI Agent"}

handler = Mangum(app)
