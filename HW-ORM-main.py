import sqlalchemy
from sqlalchemy.orm import sessionmaker

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

# принимает имя или идентификатор издателя (publisher), например, через input(). Выводит построчно факты покупки книг этого издателя:
# название книги | название магазина, в котором была куплена эта книга | стоимость покупки | дата покупки
# Пример (было введено имя автора — Пушкин):
# Капитанская дочка | Буквоед     | 600 | 09-11-2022
# Руслан и Людмила  | Буквоед     | 500 | 08-11-2022
# Капитанская дочка | Лабиринт    | 580 | 05-11-2022
# Евгений Онегин    | Книжный дом | 490 | 02-11-2022
# Капитанская дочка | Буквоед     | 600 | 26-10-2022

ent_publ = input("Введите фамилию автора: ")

subq = session.query(Shop, Sale, Stock, Book, Publisher
                    ).filter(Publisher.p_name == ent_publ
                    ).filter(Book.id_publisher == Publisher.id
                    ).filter(Stock.id_book == Book.id
                    ).filter(Sale.id_stock == Stock.id
                    ).filter(Shop.id == Stock.id_shop)
for a in subq.all():
    print(a.Book.title, a.Shop.sh_name, a.Sale.price, a.Sale.date_sale, sep='\t|')