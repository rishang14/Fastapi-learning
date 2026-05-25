from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class User(Base): 
     __tablename__= "users"  

     id = Column(Integer,primary_key=True) 
     name= Column(String(100),nullable=False) 
     email= Column(String(150),nullable=False, unique=True)  
     password=Column(String,nullable=False) 
     created_at=Column(DateTime(timezone=True), server_default=func.now())

