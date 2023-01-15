import sqlite3
from .scripts.sourse_db import Sourse_db


class DB:
    def __init__(self, config: dict[str: [str]], db_name: str, *args, **kwargs) -> None:
        self.config = config
        self.db_name = db_name
        
    def connect_to_db(self, **keys_for_db_connection) -> bool:
        if not self.db_name:
            raise ValueError('You must first specify the name of the database file.')
        
        self.base = sqlite3.connect(self.db_name, *keys_for_db_connection)
        self.cur = self.base.cursor()
        
        self.s_db = Sourse_db(self.db_name)
        
        return True
        
    def update_configure(self) -> dict[str: bool]:
        if not self.config:
            raise ValueError('First you need to specify the config!')
    
        res = {}
    
        for table in self.config:
            try:
                self.s_db.sourse_request(f"SELECT * FROM {table} LIMIT 1")
            except: 
                self.s_db.create_table(table, *self.config[table])
                res[table] = True
            else:
                res[table] = False
            
        return res

    def change_config(self, new_config: dict[str: [str]]) -> dict[str: bool]:
        self.config = new_config
        return self.update_configure()
    
    def start(self, **keys_for_db_connection) -> dict[str: bool]:
        self.connect_to_db(*keys_for_db_connection)
        return self.update_configure()