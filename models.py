import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base=declarative_base()


class Publisher(Base):
    __tablename__="publisher"
    id=sq.Column(sq.Integer, primary_key=True)
    name=sq.Column(sq.String, unique=True, nullable=False)

    books=relationship("Book", back_populates="publisher")


class Book(Base):
    __tablename__="book"
    id=sq.Column(sq.Integer, primary_key=True)
    title=sq.Column(sq.String, nullable=False)
    id_publisher=sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher=relationship("Publisher", back_populates="books")
    book_stocks=relationship("Stock", back_populates="stocks_book")

class Shop(Base):
    __tablename__="shop"
    id=sq.Column(sq.Integer, primary_key=True)
    name=sq.Column(sq.String,nullable=False)

    shops=relationship("Stock", back_populates="stocks_shop")

class Stock(Base):
    __tablename__="stock"
    id=sq.Column(sq.Integer, primary_key=True)
    count=sq.Column(sq.Integer, nullable=False)
    id_book=sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop=sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    stocks_book=relationship("Book", back_populates="book_stocks")
    stocks_shop=relationship("Shop", back_populates="shops")
    sales=relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__="sale"
    id =sq.Column(sq.Integer, primary_key=True)
    price=sq.Column(sq.REAL, nullable=False)
    date_sale=sq.Column(sq.Date, nullable=False)
    count=sq.Column(sq.Integer, nullable=False)
    id_stock=sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    stock=relationship("Stock", back_populates="sales")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



