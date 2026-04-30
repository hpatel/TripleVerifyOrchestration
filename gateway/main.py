from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

ORCHESTRATOR_URL = "http://orchestrator:8000/run"

@app.post("/query")
async def query(data: dict):
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            res = await client.post(ORCHESTRATOR_URL, json=data)
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail=res.text)
            return res.json()
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Orchestrator timeout - request took too long")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Cannot connect to orchestrator")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
