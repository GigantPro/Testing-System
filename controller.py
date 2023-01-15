from const import *
from packages.DB import DB
from json import load as j_load


class Controller:
    def __init__(self) -> None:
        self.config = self.read_config()
        
        self.db = DB(self.config, DB_NAME)
        
        self.start_db()
        
    def start_db(self) -> dict[str: bool]:
        return self.db.start()
    
    def read_config(self, path: str='config/db_conf.json') -> dict:
        with open(path, 'r', encoding='utf-8') as f: return j_load(f)