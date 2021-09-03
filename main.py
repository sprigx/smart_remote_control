from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import textwrap

app = FastAPI()

# リクエストbodyを定義
class Request(BaseModel):
    target: str
    command: str

@app.post("/control")
def control(request: Request):
    try:
        cmd = ('python3 irrp.py -p -g17 -f codes '
              f'{request.target}:{request.command}')
        res = subprocess.check_output(cmd, shell=True)
        print(cmd)
        return {"detail": "ok"}
    except:
        return {"detail": "failed"}
