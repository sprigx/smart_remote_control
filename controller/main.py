from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import textwrap
import uvicorn
import os
from test import Test
from remote_controller import RemoteController

def build_filepath(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

app = FastAPI()

# define the request body.
class Request(BaseModel):
    target: str
    command: str

@app.post("/control")
async def control(request: Request):
    try:
        # cmd = (f"python3 {build_filepath('irrp.py')} -p -g17 -f {build_filepath('codes')} "
        #        f'{request.target}:{request.command}')
        # res = subprocess.check_output(cmd, shell=True)
        # print(cmd)
        c.transmit(request.target, request.command)
        return {"detail": "ok"}
    except:
        return {"detail": "failed"}

@app.get("/test")
async def test():
    return {"detail": "this is a test."}

@app.on_event("shutdown")
async def shutdown_event():
    logger.info('Shutting down the server.')
    c.cleanup()

if __name__ == '__main__':
    c = RemoteController(17)
    logger = logging.getLogger('uvicorn')
    uvicorn.run(app, host='0.0.0.0', port=8000)
