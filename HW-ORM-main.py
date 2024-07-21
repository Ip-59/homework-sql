import sqlalchemy
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import datetime

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:196788@localhost:5432/hw_orm'

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher_1 = Publisher(p_name = "Пушкин")

book_1 = Book(title = 'Капитанская дочка', id_publisher = 1)
book_2 = Book(title = 'Руслан и Людмила', id_publisher = 1)
book_3 = Book(title = 'Евгений Онегин', id_publisher = 1)

shop_1 = Shop(sh_name = "Буквоед")
shop_2 = Shop(sh_name = "Лабиринт")
shop_3 = Shop(sh_name = "Книжный дом")

stock_1 = Stock(id_book = 1, id_shop = 1, count = 1)
stock_2 = Stock(id_book = 2, id_shop = 1, count = 1)
stock_3 = Stock(id_book = 1, id_shop = 2, count = 1)
stock_4 = Stock(id_book = 3, id_shop = 3, count = 1)
stock_5 = Stock(id_book = 1, id_shop = 2, count = 1)

sale_1 = Sale(price = 600, date_sale = '09-11-2022', id_stock = 1, count = 1) #Капитанская дочка| Буквоед
sale_2 = Sale(price = 500, date_sale = '08-11-2022', id_stock = 2, count = 1) #Руслан и Людмила  | Буквоед
sale_3 = Sale(price = 580, date_sale = '05-11-2022', id_stock = 3, count = 1) #Капитанская дочка | Лабиринт
sale_4 = Sale(price = 490, date_sale = '02-11-2022', id_stock = 4, count = 1) #Евгений Онегин    | Книжный дом
sale_5 = Sale(price = 600, date_sale = '26-10-2022', id_stock = 1, count = 1) #Капитанская дочка | Буквоед

session.add_all([publisher_1, book_1, book_2, book_3, shop_1, shop_2, shop_3])
session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5])
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5])

session.commit()


def get_shops(publisher):
    
    q = session.query(
        Publisher.id, Publisher.p_name, Book.title, Shop.sh_name, Sale.price, Sale.date_sale
    ).select_from(Shop). \
    join(Stock, Shop.id == Stock.id_shop).\
    join(Book, Stock.id_book == Book.id).\
    join(Publisher, Book.id_publisher == Publisher.id).\
    join(Sale, Sale.id_stock == Stock.id)

    if publisher.isdigit(): #Проверяем переданные данные в функцию на то, что строка состоит только из чисел
        shops = q.filter(Publisher.id == publisher).all() #Обращаемся к запросу, который составили ранее, и фильтруем по id
    else:
        shops = q.filter(Publisher.p_name == publisher).all() #Обращаемся к запросу, который составили ранее, и фильтруем по фамилии автора

    for p_name, p_id, title, name, price, date_sale in shops: 
        print(f"{title: <17} | {name: <11} | {price: <3} | {date_sale.strftime('%d-%m-%Y')}")


if __name__ == '__main__':

    ent_publ = input("Введите фамилию или id автора: ")
    get_shops(ent_publ)
