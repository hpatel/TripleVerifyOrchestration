from fastapi import FastAPI
from index_manager import DB

app = FastAPI()
db = DB()

@app.post("/add")
async def add(data: dict):
    db.add(data["text"])
    return {"ok": True}

@app.post("/search")
async def search(data: dict):
    return {"context": db.search(data["query"])}