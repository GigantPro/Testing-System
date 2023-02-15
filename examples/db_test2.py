from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alchemy_decl import Base, Book, Author

engine = create_engine("mysql+mysqlconnector://root:root@localhost/pylounge2", echo=True)
# Флаг echo включает ведение лога через стандартный модуль logging Питона.
# Когда он включен, мы увидим все созданные нами SQL-запросы. 
session = sessionmaker(bind=engine)
s = session()

author_one = Author(name="Лутц") 
s.add(author_one) 
s.commit()

author_one = Author(name="НеЛутц") 
s.add(author_one) 
s.commit()

book_one = Book(title="Чистый Python", author_id=1, genre="компьютерная литература", price=1500) 
s.add(book_one) 
s.commit()

s.add_all([Book(title="Чистый Чистый Python", author_id=1, genre="компьютерная литература", price=500),
           Book(title="НеЧистый Python", author_id=2, genre="компьютерная литература", price=2500),
           Book(title="Python как Питон", author_id=1, genre="компьютерная литература", price=2976)  
           ])
s.commit()

print(s.query(Book).first().title)

for title, price in s.query(Book.title, Book.price).order_by(Book.title).limit(2):
    print(title, price)

print('\n\n\n')

for row in s.query(Book, Author).filter(Book.author_id == Author.id_author).filter(Book.price > 1000).group_by(Author.name):
    print(row.Book.title, ' ', row.Author.name)

print('\n\n\n')

print([(row.Book.title, row.Author.name) for row in s.query(Book, Author).join(Author).all()])

autor_query = s.query(Author).filter_by(Author.name == 'НеЛутц').one()
if autor_query != []:
    autor_query.name = 'Бизли' 
    s.add(autor_query)
    s.commit()
