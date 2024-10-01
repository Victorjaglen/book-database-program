from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///suggested_books.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Books(Base):

    __tablename__ = 'suggested_books'

    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    date_published = Column('date_published', Date)
    price = Column('Price', Integer)

    def __repr__(self):
        return f"Title={self.title}, Author={self.author}, date_published={self.date_published}, price={self.price}"


# if __name__ == "__main__":
#     Base.metadata.create_all(engine)


# create a database
# books.db
# create a model
# title, author, date published, price