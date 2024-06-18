import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
SUBD='postgresql'
USER_PASS='posgres:110'
BD_NAME='office'
# DSN='postgresql://postgres:110@localhost:5432/office'
DSN=SUDB + '://' + USER_PASS + '@localhost:5432' + '/' + BD_NAME
# engine=sqlalchemy.create_engine(DSN, echo=True)
engine=sqlalchemy.create_engine(DSN)
create_tables(engine)

Session=sessionmaker(bind=engine)
session=Session()
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

session.commit()
s_input=input('Enter publisher name :')
subq1=session.query((Book.id).label('book_id'), Book.title).join(Publisher.books).filter(Publisher.name.like('%'+ s_input+'%')).subquery()
subq2=session.query((Stock.id).label('stock_id'), Stock.id_book, Shop.name, subq1.c.title).join(subq1, subq1.c.book_id==Stock.id_book).join(Shop, Stock.id_shop==Shop.id).subquery()
widht_fields=[]
widht_fields.append(session.query(sqlalchemy.func.max(sqlalchemy.func.char_length(Book.title))).one()[0])
widht_fields.append(session.query(sqlalchemy.func.max(sqlalchemy.func.char_length(Shop.name))).one()[0])
widht_fields.append(10)
widht_fields.append(10)
for c in session.query(Sale.id, sqlalchemy.func.to_char(Sale.date_sale, 'DD-MM-YYYY'), (Sale.price*Sale.count), subq2.c.title, subq2.c.name).join(subq2, subq2.c.stock_id==Sale.id_stock).all():
    print(c[3].ljust(widht_fields[0]+2) + '|' + c[4].ljust(widht_fields[1]+2) + '|' + str(c[2]).center(widht_fields[2]) + '|' +c[1].center(widht_fields[3]))
session.close
 