import socket
from fastapi import Cookie, FastAPI
from fastapi import FastAPI, Response, Request
import uvicorn
import hashlib
import random
from time import time
from datetime import datetime as dt
from const import *
from loguru import logger
from controller import Controller
from fastapi.responses import RedirectResponse, PlainTextResponse

controller = Controller()

app = FastAPI()

@app.get('/')
def read_root():
    return RedirectResponse("/docs")

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post('/init')
def login(response: Response, request: Request, token=Cookie()):
    if token:
        res = controller.db.read_line('tokens', 'token', token)
        if res:
            if token == res[1] and res[5] == True:
                response.set_cookie(key='last_ip', value=client_host)  
                print(1)
                return {'sucscess'}
    
    
    time_now = time()
    random_value = str(random.random())
    client_host = request.client.host
    
    token = hashlib.sha256(f'{time_now}{random_value}{client_host}'.encode('utf-8')).hexdigest()
    response.set_cookie(key='token', value=token)
    response.set_cookie(key='last_ip', value=client_host)
    
    controller.db.add_value('tokens', None, token, str(dt.now()).split('.')[0], None, client_host, True)
    
    return {'sucscess'}




if __name__ == '__main__':
    ip = IP
    
    if not ip:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
            except:
                logger.warning('ERROR: Нет подключение к интернету. Повторная попытка через 5 сек.')
                time.sleep(5)
    
    uvicorn.run('main:app', port=8000, host=ip, reload=True)


class WEB_parser:
    def __init__(self) -> None:
        pass