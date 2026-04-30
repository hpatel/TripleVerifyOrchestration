import httpx
from fastapi import HTTPException
from fastapi import FastAPI
import os

print("======== ENV DEBUG ========")
MEMORY_URL = os.environ.get("MEMORY_URL")
print("MEMORY_URL:", MEMORY_URL)
print("===========================")

app = FastAPI()

@app.post("/retrieve")
async def retrieve(data: dict):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.post(MEMORY_URL, json=data)

            if res.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Memory service error: {res.text}"
                )

            if not res.text.strip():
                raise HTTPException(
                    status_code=500,
                    detail="Empty response from memory service"
                )

            try:
                payload = res.json()
            except Exception:
                raise HTTPException(
                    status_code=500,
                    detail=f"Invalid JSON from memory service: {res.text[:200]}"
                )

            if "context" not in payload and "memories" not in payload:
                raise HTTPException(
                    status_code=500,
                    detail=f"Missing 'context' or 'memories' in response: {payload}"
                )

            context = payload.get("context", payload.get("memories", []))
            return {"context": context}

        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to memory service"
            )