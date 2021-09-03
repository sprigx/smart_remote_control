from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/control")
async def control(target, command):
    try:
        res = subprocess.check_output(f'python3 irrp.py -p -g17 -f codes {target}:{command}', shell=True)
        return {"detail": "ok"}
    except:
        return {"detail": "failed"}
