<<<<<<< HEAD
from fastapi import FastAPI
from .graph import build

app = FastAPI()
graph = build()

@app.post("/run")
async def run(data: dict):
    result = await graph.ainvoke(data)
=======
from fastapi import FastAPI
from graph import build
import sys
import os

sys.path.append(os.path.dirname(__file__))

app = FastAPI()
graph = build()

@app.post("/run")
async def run(data: dict):
    result = await graph.ainvoke(data)
>>>>>>> 957bc36 (Moving all config to .env file. Improvig dependency install time by using uv. Fix minor port issues.)
    return result