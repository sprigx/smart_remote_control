from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import textwrap
import uvicorn
import os
import logging
from remote_controller import RemoteController

def build_filepath(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

app = FastAPI()
c = RemoteController(17)
logger = logging.getLogger('uvicorn')

# define the request body.
class Request(BaseModel):
    target: str
    command: str

@app.post("/control")
async def control(request: Request):
    try:
        res = c.transmit(request.target, request.command)
        logger.info(res)
        return {"detail": "ok"}
    except:
        return {"detail": "failed"}

@app.get("/test")
async def test():
    return {"detail": "this is a test."}

@app.on_event("shutdown")
async def shutdown_event():
    c.cleanup()
    logger.info('Finished RemoteController cleaning up.')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, lifespan='on')
