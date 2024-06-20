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
# create_tables(engine)
#
# Session=sessionmaker(bind=engine)
# session=Session()
# with open("test.json", encoding="utf-8") as f:
#     json_data=json.load(f)
# for v in json_data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale
#     }[v.get('model')]
#     session.add(model(id=v.get('pk'), **v.get('fields')))

# session.commit()

def get_shops(publisher_info): #Функция принимает обязательный параметр
    qry = db_session.query( #Создаем общее тело запроса на выборку данных и сохраняем в переменную
        Book.title, Shop.name, (Sale.price * Sale.count).label('total_sale'), Sale.date_sale #Название книги, имя магазина, стоимость продажи и дату продажи
    ).select_from(Shop).\ #Из таблицы магазинов
        join(Stock, Stock.id_shop=Shop.id).\ #Объединяем с таблицей стоков
        join(Book, Book.id=Stock.id_book).\ #Объединяем с таблицей книг
        join(Publisher, Publisher.id=Book.id_publisher).\ #Объединяем с таблицей публицистов
        join(Sale, Sale.id_stock=Stock.id) #Объединяем с таблицей продаж
    if publisher_info.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        qry_end = qry.filter(Publisher.id == int(publisher_info)).all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где айди публициста равно переданным данным в функцию, и сохраняем в переменную
    else:
        qry_end= qry.filter(Publisher.id == 'publisher_info').all() #Обращаемся к запросу, который составили ранее, и применяем фильтрацию, где имя публициста равно переданным данным в функцию, и сохраняем в переменную
    for c in qry_end: #Проходим в цикле по переменой, в которой сохраняем результат фильтрации, и при каждой итерации получаем кортеж и распаковываем значения в 4 переменные
        print(f"{c[0]: <40} | {c[1]: <10} | {c[2]: <8} | {c[3].strftime('%d-%m-%Y')}") #Передаем в форматированную строку переменные, которые содержат имя книги, название магазина, стоимость продажи и дату продажи


if __name__ == '__main__':
    s = input("Enter publisher name or publisher id: ") #Просим клиента ввести имя или айди публициста и данные сохраняем в переменную
    get_shops(s) #Вызываем функцию получения данных из базы, передавая в функцию данные, которые ввел пользователь строкой выше

# s_input=input('Enter publisher name :')
# subq1=session.query((Book.id).label('book_id'), Book.title).join(Publisher.books).filter(Publisher.name.like('%'+ s_input+'%')).subquery()
# subq2=session.query((Stock.id).label('stock_id'), Stock.id_book, Shop.name, subq1.c.title).join(subq1, subq1.c.book_id==Stock.id_book).join(Shop, Stock.id_shop==Shop.id).subquery()
# widht_fields=[]
# widht_fields.append(session.query(sqlalchemy.func.max(sqlalchemy.func.char_length(Book.title))).one()[0])
# widht_fields.append(session.query(sqlalchemy.func.max(sqlalchemy.func.char_length(Shop.name))).one()[0])
# widht_fields.append(10)
# widht_fields.append(10)
# for c in session.query(Sale.id, sqlalchemy.func.to_char(Sale.date_sale, 'DD-MM-YYYY'), (Sale.price*Sale.count), subq2.c.title, subq2.c.name).join(subq2, subq2.c.stock_id==Sale.id_stock).all():
#     print(c[3].ljust(widht_fields[0]+2) + '|' + c[4].ljust(widht_fields[1]+2) + '|' + str(c[2]).center(widht_fields[2]) + '|' +c[1].center(widht_fields[3]))
session.close
