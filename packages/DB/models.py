from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy import create_engine
from json import load


config = {
    "ip": "192.168.1.96",
    "login": "testingsysusr",
    "passwd": "~8nHK{nfTB6sVg6aWoXsA%nt{wja!r",
    "port": "5432",
    "basename": "testingsystem",
    "typeconnect": "postgresql"
}

print(config)

SQLALCHEMY_DATABASE_URL = f"{config['typeconnect']}://{config['login']}:{config['passwd']}@{config['ip']}:{config['port']}/{config['basename']}"
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()

class User_DB(Base): 
    __tablename__ = "users"
    
    user_id      = Column(Integer, primary_key=True, index=True)
    login        = Column(String)
    password     = Column(String)
    phone_number = Column(String)
    email        = Column(String)
    age          = Column(Integer)
    first_name   = Column(String)
    second_name  = Column(String)    
    last_name    = Column(String)    
    created_time = Column(DateTime)


class Logger(Base):
    __tablename__ = "logger"
    
    log_id      = Column(Integer, primary_key=True, index=True)
    log_type    = Column(String)
    initiator   = Column(String)
    target      = Column(String)
    time        = Column(DateTime)


Base.metadata.create_all(engine)  