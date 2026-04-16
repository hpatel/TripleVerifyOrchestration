from fastapi import FastAPI
import httpx

app = FastAPI()

ORCHESTRATOR_URL = "http://orchestrator:8000/run"

@app.post("/query")
async def query(data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(ORCHESTRATOR_URL, json=data)
        return res.json()