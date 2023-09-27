from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime 


Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    # Relationship with BorrowRecord
    borrow_records = relationship('BorrowRecord', back_populates='book')


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Define the Enum for class year
    class_year = Column(Enum('First_year', 'Second_year', 'Third_year', 'Fourth_year'), nullable=False)

    # Relationship with BorrowRecord
    borrow_records = relationship('BorrowRecord', back_populates='student')


class BorrowRecord(Base):
    __tablename__ = 'borrow_records'

    record_id = Column(Integer, primary_key=True)
    borrow_date = Column(Date)
    return_date = Column(Date)
    student_id = Column(Integer, ForeignKey('students.id')) 
    book_id = Column(Integer, ForeignKey('books.id'))

    # relationship 
    student = relationship('Student', back_populates='borrow_records')
    book = relationship('Book', back_populates='borrow_records')


engine = create_engine('sqlite:///library.db', echo=True)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


## Seeding
# book1 = Book(id=1, title="Elements of Pyromancy", author="Baltazar David")
# book2 = Book(id=2, title="Nightmare Tales", author="Lysandra Ruthdock")
# book3 = Book(id=3, title="Eldershrine for Undead", author="Thelen")
# book4 = Book(id=4, title="Montua", author="Wewine Collins")
# book5 = Book(id=5, title="How to Kill a Vampire", author="Ruth Ennick")
# book6 = Book(id=6, title="Spirits and Cycles of the Moon", author="Tzaycde")
# book7 = Book(id=7, title="Ywyne Herbs and Potions", author="Kodduck Bloomcy")


# student1 = Student(id=1, name="Tri React", class_year="First_year")
# student2 = Student(id=2, name="Juan Diego Juanov", class_year="First_year")
# student3 = Student(id=3, name="Kam TopDanger Havi", class_year="Third_year")

# session.add_all([book1, book2, book3, book4, book5, book6, book7, student1, student2, student3])
# session.commit()

