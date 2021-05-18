from sqlalchemy import MetaData, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = declarative_base()

metadata = MetaData()

class User(Base):
    __tablename__ = "all_users"
    
    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer)
    username = Column("username", String(255))
    date_registration = Column("date_registration", String)
    language = Column("language", String)
    balance = Column("balance", String)

    def __repr__(self):
        return "<User {0} {1} {2} {3} {4} {5}>".format(
                self.id, self.user_id, 
                self.username, self.date_registration, 
                self.language, self.balance,
        )

class DataUser(Base):
    __tablename__ = "data_users"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer)
    date = Column("date", String)
    status = Column("status", String)
    last_phone = Column("last_phone", String)
    last_date = Column("last_date", String)

    def __repr__(self):
        return "<Data user {0} {1} {2} {3} {4} {5}>".format(
                self.id, self.user_id, 
                self.date, self.status, 
                self.last_phone, self.last_date
        )

class Orders(Base):
        __tablename__ = "phone_all_orders"

        id = Column("id", Integer, primary_key=True)
        user_id = Column("user_id", Integer)
        created = Column("created", String)
        service = Column("service", String)
        price = Column("price", String)

        def __repr__(self):
                return "<Order {0} {1} {2} {3} {4}>".format(
                        self.id, self.user_id, 
                        self.created, self.service, 
                        self.price
                )

engine = create_engine("sqlite:///database/data_bomber.db")
Base.metadata.create_all(engine)
session = Session(bind=engine)