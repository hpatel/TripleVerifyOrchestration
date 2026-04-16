from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.post("/execute")
async def run(data: dict):
    code = data.get("code", "")
    res = subprocess.run(["python","-c",code],capture_output=True,text=True)
    return {"stdout": res.stdout, "stderr": res.stderr}