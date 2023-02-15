from sqlalchemy import Column, ForeignKey, Integer, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship  
from sqlalchemy import create_engine  

engine = create_engine("mysql+mysqlconnector://root:root@localhost/pylounge2", echo=True)

Base = declarative_base()  

class Book(Base):  
    __tablename__ = 'Books'  
    
    id_book = Column(Integer, primary_key=True)  
    title = Column(String(250), nullable=False)  
    author_id = Column(Integer, ForeignKey("Authors.id_author"))  
    genre = Column(String(250))
    price = Column(Integer, nullable=False)
    Author = relationship("Author") 

class Author(Base):  
    __tablename__ = 'Authors'  
    
    id_author = Column(Integer, primary_key=True)  
    name = Column(String(250), nullable=False)  
    book = relationship("Book") # 1 ко многим

Base.metadata.create_all(engine)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          