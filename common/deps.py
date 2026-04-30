import socket
import asyncio
import httpx

async def check_http(url: str, timeout=3):
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url)
            return r.status_code < 500
    except Exception:
        return False


def check_tcp(host: str, port: int, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False