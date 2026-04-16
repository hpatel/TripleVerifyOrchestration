import redis
from index_manager import DB

r = redis.Redis(host="redis", port=6379)
db = DB()

while True:
    msgs = r.xread({"rag": "0-0"}, block=0)
    for _, m in msgs:
        for _, d in m:
            db.add(d[b"text"].decode())