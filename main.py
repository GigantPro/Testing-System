import socket
from fastapi import FastAPI
from fastapi import FastAPI, Response, Request
import uvicorn
import hashlib
import random
from time import time
from const import *
from loguru import logger
from controller import Controller

controller = Controller()

app = FastAPI()

@app.get('/')
def read_root():
    return {'not usable'}

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post('/init')
def login(response: Response, request: Request):
    time_now = time()
    random_value = str(random.random())
    client_host = request.client.host
    
    token = hashlib.sha256(f'{time_now}{random_value}{client_host}').hexdigest()
    response.set_cookie(key='token', value=token)
    response.set_cookie(key='last_ip', value=client_host)
    
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