import httpx

async def call(url: str, payload: dict):
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, json=payload)

        # 🚨 Check HTTP status FIRST
        if r.status_code != 200:
            raise Exception(
                f"Service call failed: {url}\n"
                f"Status: {r.status_code}\n"
                f"Response: {r.text}"
            )

        # 🚨 Ensure response is not empty
        if not r.content:
            raise Exception(f"Empty response from {url}")

        # 🚨 Safe JSON parsing
        try:
            return r.json()
        except Exception:
            raise Exception(
                f"Invalid JSON from {url}\n"
                f"Raw response: {r.text[:500]}"
            )