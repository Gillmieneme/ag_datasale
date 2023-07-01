from sqlalchemy import Column, Integer, String, Boolean
from .database import base
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE
from sqlalchemy.sql.expression import text
from sqlalchemy import func
from sqlalchemy.orm import column_property


class Income(base):
    __tablename__="income"
    
    id= Column(Integer,primary_key=True,nullable=False)
    is_deleted=Column(Boolean,nullable=False,server_default='0')
    user_id=Column(Integer,nullable=False)
    dates=Column(DATE, nullable=False,)
    type_val=Column(Integer,nullable=False)
    detail=Column(String(100),nullable=False)
    amount =Column(Integer,nullable=False)
    formatted_datetime = column_property(func.to_char(dates, "DD-MM-YYYY"))
    

class User(base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,nullable=False) 
    username=Column(String(100),nullable=False,unique=True)
    password=Column(String(400),nullable=False)


