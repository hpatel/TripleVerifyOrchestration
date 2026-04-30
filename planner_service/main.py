from fastapi import FastAPI

app = FastAPI()

@app.post("/plan")
async def plan(data: dict):
    return {"plan": f"Breakdown: {data['query']}"}