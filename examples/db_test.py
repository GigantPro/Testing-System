from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, and_

#######################################################################################
# без связывания с классами 

engine = create_engine("mysql+mysqlconnector://root:root@localhost/pyloungedb", echo=True)
meta = MetaData(engine)

authors = Table('Authors', meta, autoload=True) 
books = Table('Books', meta, autoload=True) 

conn = engine.connect()
s = select([books, authors]).where(and_(books.c.author_id == authors.c.id_author, books.c.price > 1200))
result = conn.execute(s)

for row in result.fetchall():
   print (row)

# удление записи
delete_query = books.delete().where(books.c.id_book == 1) # DELETE Books WHERE BOKKS.ID_BOOK == 1;
conn.execute(delete_query)

# обнолвение записи
update_query=books.update().where(books.c.id_book==2).values(title='AnotherTitle') # UPDATE books SET title= al where books.id_book=3;
conn.execute(update_query)


#############################################################################################
# связываем с классами
from sqlalchemy.orm import mapper, relationship, sessionmaker

engine = create_engine("mysql+mysqlconnector://root:root@localhost/pyloungedb", echo=True)
meta = MetaData(engine)

authors = Table('Authors', meta, autoload=True) 
books = Table('Books', meta, autoload=True) 

class Book(object):
    def __init__(self, title, author_id, genre, price):
        self.title = title
        self.author_id = author_id
        self.genre = genre
        self.price = price

    def __repr__(self):
        return "<Book('%s','%s', '%s', '%s')>" % (self.title, str(self.author_id), 
                                            self.genre, str(self.price))

class Author():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Author('%s')>" % (self.name)

mapper(Book, books)
mapper(Author, authors)

new_book = Book("NewBook", 1, "NewG", 2500)

DBSession = sessionmaker(bind=engine)
session = DBSession()
session.add(new_book)
session.commit() # session.rollback() - откат 

for row in session.query(Book).filter(Book.price > 1000): 
    print (row.title)

#Последовательное выполнение методов sqlalchemy.orm.query.Query.filter() соединяет условия WHERE при помощи оператора AND, аналогично конструкции select().where()
for row in session.query(Book, Author).filter(Book.author_id == Author.id_author).filter(Book.price > 1000):
    print(row.Book.title, ' ', row.Author.name)

print()
# обновление записи
second_book = session.query(Book).filter_by(id_book=3).one()
if second_book != []:
    second_book.price = 3000 
    session.add(second_book)
    session.commit()

second_book = session.query(Book).filter_by(id_book=2).one()
if second_book:
    print(second_book)
    # удаление
    session.delete(second_book)
    session.commit()

try:
    query_res = session.query(Book).filter_by(id_book=2).one()
except Exception as e:
    print(e)
else:
    print(query_res.price)