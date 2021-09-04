from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import textwrap
import uvicorn
import os
from test import Test

def build_filepath(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

app = FastAPI()

# リクエストbodyを定義
class Request(BaseModel):
    target: str
    command: str

@app.post("/control")
def control(request: Request):
    try:
        cmd = (f'python3 {build_filepath('irrp.py')} -p -g17 -f codes '
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
