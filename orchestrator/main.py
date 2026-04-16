from fastapi import FastAPI
from .graph import build

app = FastAPI()
graph = build()

@app.post("/run")
async def run(data: dict):
    result = await graph.ainvoke(data)
    return result