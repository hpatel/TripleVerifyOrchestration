from fastapi import FastAPI

app = FastAPI()

@app.post("/critic")
async def critic(data: dict):
    return {"score": 0.9}