import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    p_name = sq.Column(sq.String(length=40), nullable=False, unique=True)

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False, unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    sh_name = sq.Column(sq.String(length=40), nullable=False, unique=True)    

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Numeric(9,2))
    date_sale = sq.Column(sq.String(length=10))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



#ent_publ = input("Введите фамилию автора: ")

# session.close()

# import sqlalchemy
# import sqlalchemy as sq
# from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Base = declarative_base()


# class Course(Base):
#     __tablename__ = "course"

#     id = sq.Column(sq.Integer, primary_key=True)
#     name = sq.Column(sq.String(length=40), unique=True)

#     # homeworks = relationship("Homework", back_populates="course")


# class Homework(Base):
#     __tablename__ = "homework"

#     id = sq.Column(sq.Integer, primary_key=True)
#     number = sq.Column(sq.Integer, nullable=False)
#     description = sq.Column(sq.Text, nullable=False)
#     course_id = sq.Column(sq.Integer, sq.ForeignKey("course.id"), nullable=False)

#     # course = relationship(Course, back_populates="homeworks")
#     course = relationship(Course, backref="homeworks")


# def create_tables(engine):
#     # Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)


# DSN = "postgresql://postgres:postgres@localhost:5432/netology_db"
# engine = sqlalchemy.create_engine(DSN)
# create_tables(engine)

# # сессия
# Session = sessionmaker(bind=engine)
# session = Session()

# # создание объектов
# js = Course(name="JavaScript")
# print(js.id)
# hw1 = Homework(number=1, description="первое задание", course=js)
# hw2 = Homework(number=2, description="второе задание (сложное)", course=js)

# session.add(js)
# print(js.id)
# session.add_all([hw1, hw2])
# session.commit()  # фиксируем изменения
# print(js.id)


# # запросы
# q = session.query(Course).join(Homework.course).filter(Homework.number == 1)
# print(q)
# for s in q.all():
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)

# # вложенный запрос
# subq = session.query(Homework).filter(Homework.description.like("%сложн%")).subquery("simple_hw")
# q = session.query(Course).join(subq, Course.id == subq.c.course_id)
# print(q)
# for s in q.all():/
#     print(s.id, s.name)
#     for hw in s.homeworks:
#         print("\t", hw.id, hw.number, hw.description)


# # обновление объектов
# session.query(Course).filter(Course.name == "JavaScript").update({"name": "NEW JavaScript"})
# session.commit()  # фиксируем изменения


# # удаление объектов
# session.query(Homework).filter(Homework.number > 1).delete()
# session.commit()  # фиксируем изменения
