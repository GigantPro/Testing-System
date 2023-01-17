import sqlite3
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


class Sourse_db:
    # def __init__(self, base_name: str) -> None:
    #     SQLALCHEMY_DATABASE_URL = f"sqlite:///{base_name}"
    #     # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"  Потом юзать, пока что не надо
        

    #     self.engine = create_engine(
    #         SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    #     )
    #     self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    #     self.Base = declarative_base()
    
    def __init__(self, base_name: str) -> None:
        self.base = sqlite3.connect(base_name, check_same_thread=False)
        self.cur = self.base.cursor()
        if not self.base:
            raise ConnectionError('Error to connection DB')
    
    def create_table(self, name: str, *arg) -> None:
        self.base.execute('CREATE TABLE IF NOT EXISTS {}({})'.format(name, ', '.join(arg)))
        self.base.commit()

    def add_value(self, tabel_name: str, *values) -> None:
        self.cur.execute('INSERT INTO {} VALUES({})'.format(tabel_name, ', '.join(['?' for _ in range(len(values))])), tuple(values))
        self.base.commit()

    def read_all_from_table(self, tabel_name: str) -> list:
        return self.base.execute(f"SELECT * FROM {tabel_name}").fetchall()

    def read_line(self, tabel_name: str, colum_name: str, value: str):
        return self.base.execute("SELECT * FROM {} WHERE {} == ?".format(tabel_name, colum_name), (value,)).fetchone()

    def read_lines(self, tabel_name: str, colum_name: str, value: str):
        return self.base.execute("SELECT * FROM {} WHERE {} == ?".format(tabel_name, colum_name), (value,)).fetchall()

    def update_value(self, tabel_name: str, flag_value: str, colum_flag_name: str, new_value: str, colum_new_name: str) -> None:
        self.cur.execute('UPDATE {} SET {} == ? WHERE {} == ?'.format(tabel_name, colum_new_name, colum_flag_name), (new_value, flag_value))
        self.base.commit()

    def delete_line(self, table_name: str, flag_colum_name: str, flag_value: str) -> None:
        self.cur.execute('DELETE FROM {} WHERE {} == ?'.format(table_name, flag_colum_name), (flag_value,))
        self.base.commit()
    
    def sourse_request(self, reguest: str) -> sqlite3.Cursor:
        res = self.cur.execute(reguest)
        self.base.commit()
        return res