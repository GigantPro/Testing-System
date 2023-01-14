import sqlite3
from .scripts.sourse_db import SourseDB


class DB:
    def __init__(self, *, config: dict[str: [str]]=None, db_name: str=None) -> None:
        self.config = config
        self.db_name = db_name
        
    def connect_to_db(self, **keys_for_db_connection) -> bool:
        if not self.db_name:
            raise ValueError('You must first specify the name of the database file.')
        
        self.base = sqlite3.connect(self.db_name, *keys_for_db_connection)
        self.cur = self.base.cursor()
        
        self.SourseDB = SourseDB(self.db_name)
        
        return True
        
    def update_configure(self) -> dict[str: bool]:
        if not self.config:
            raise ValueError('First you need to specify the config!')
    
        res = {}
    
        for table in self.config:
            if self.SourseDB.sourse_request(f"SHOW TABLES LIKE '{table}'").fetchone():
                res[table] = False
                continue
            self.SourseDB.create_table(table, *self.config[table])
            res[table] = True
            
        return res