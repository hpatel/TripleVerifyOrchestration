from fastapi import FastAPI
import redis, json, os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

@app.post("/get")
async def get(data: dict):
    mem = r.lrange("memory", 0, -1)
    return {"memories": [json.loads(m) for m in mem]}

@app.post("/add")
async def add(data: dict):
    r.rpush("memory", json.dumps(data))
    return {"ok": True}