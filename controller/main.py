from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import textwrap
import uvicorn
from test import Test

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

@app.get("/test")
def test():
    plus = gpio_handler.execute('+')
    minus = gpio_handler.execute('-')
    return {"detail": {"plus": plus, "minus": minus}}

if __name__ == '__main__':
    gpio_handler = Test()
    uvicorn.run(app, host='0.0.0.0', port=8000)
