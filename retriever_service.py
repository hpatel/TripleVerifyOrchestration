from fastapi import FastAPI
import httpx

app = FastAPI()
RAG_URL = "http://rag:8007/search"

@app.post("/retrieve")
async def retrieve(data: dict):
    async with httpx.AsyncClient() as client:
        res = await client.post(RAG_URL, json=data)
        return {"context": res.json()["context"]}