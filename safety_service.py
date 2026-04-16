from fastapi import FastAPI

app = FastAPI()

@app.post("/safety")
async def safety(data: dict):
    return {"score": 0.95}