from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from models import Server, Proc
import db
import hashlib
import secrets

app = FastAPI()
security = HTTPBasic()

def hash_sha224(dat):
    return hashlib.sha224(dat.encode()).hexdigest()

templates = Jinja2Templates(directory='templates')
jinja_env = templates.env

def login(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

def api_servers(request: Request):
    servers = db.session.query(Server).all()
    db.session.close()
    return servers

def api_procs(request: Request):
    procs = db.session.query(Proc).all()
    db.session.close()
    return procs

def server_state(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    passhash = '604ea986ff8a3c8671de50812d3b1c97bb1ac2fbac71388019b0a36f'
    username = 'snd'
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(hash_sha224(credentials.password), passhash)

    if not(correct_username and correct_password):
        raise HTTPException(
               status_code=HTTP_401_UNAUTHORIZED,
               detail='ユーザー名かパスワードが不正です',
               headers={'WWW-Authenticate': 'Basic'}
        )

    servers = db.session.query(Server).all()#.filter(Server.status==0).all()
    procs = db.session.query(Proc).filter(Proc.pid == 1000).all()
    db.session.close()
    return templates.TemplateResponse('admin.html', {'request': request, 'servers': servers, 'procs': procs})
