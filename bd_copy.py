import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
SUBD = 'postgresql'
USER_PASS = 'postgres:110'
BD_NAME = 'office'
HOST = 'localhost'
PORT = '5432'
# DSN='postgresql://postgres:110@localhost:5432/office'
DSN=SUBD + '://' + USER_PASS + '@' + HOST + ':' + PORT + '/' + BD_NAME
#engine=sqlalchemy.create_engine(DSN, echo=True)
engine=sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
with open("test.json", encoding="utf-8") as f:
    json_data=json.load(f)
for v in json_data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale
    }[v.get('model')]
    session.add(model(id=v.get('pk'), **v.get('fields')))

session.commit
s=input('Enter ID or NAME publisher:')
qry=session.query(Book.title, Shop.name, (Sale.price * Sale.count).label('total_sale'), Publisher.id, Publisher.name, Sale.date_sale).select_from(Stock).\
        join(Shop, Shop.id == Stock.id_shop).\
        join(Book, Book.id == Stock.id_book).\
        join(Publisher, Publisher.id == Book.id_publisher).\
        join(Sale, Sale.id_stock == Stock.id).filter(Publisher.id == int(s) if s.isdigit() else Publisher.name == s).all()
for c in qry:
    print(f"{c[0]: <40} | {c[1]: <10} | {c[2]: <8} | {c[5].strftime('%d-%m-%Y')}")
session.close
