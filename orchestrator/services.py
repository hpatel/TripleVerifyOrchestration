import httpx

async def call(url, payload):
    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload, timeout=30)
        return r.json()