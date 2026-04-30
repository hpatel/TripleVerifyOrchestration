import requests

API_URL = "http://localhost:8000/query"


def run_query(payload: dict):
    """Standard blocking request"""
    res = requests.post(API_URL, json=payload, timeout=300)

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()


def stream_query(payload: dict):
    """Streaming response (if backend supports it)"""
    with requests.post(API_URL, json=payload, stream=True, timeout=300) as res:
        if res.status_code != 200:
            raise Exception(res.text)

        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                yield chunk.decode("utf-8")