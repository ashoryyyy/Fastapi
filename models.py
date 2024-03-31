from databas import Base
from sqlalchemy import Column, Integer, String , Boolean , ForeignKey




class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    admin = Column(Boolean , default= False)
    havashenas = Column(Boolean , default= False)
    city = Column(String , ForeignKey("city.id"))

class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True )
    date = Column(String)
    status = Column(String)

