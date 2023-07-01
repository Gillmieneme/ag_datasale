from pydantic import BaseModel, validator
from datetime import date,datetime
from typing import Optional
from pydantic.types import conint

class Income(BaseModel):
    
    dates:date
    type_val:int
    detail:str 
    amount:int
    @validator("dates", pre=True)
    def prase_formatted_datetime(cls, value):
        return datetime.strptime(
            value,
             "%d-%m-%Y"
        )
    

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

class UserCreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class UserResponce(BaseModel):
    id:int
    username:str
    class Config:
        orm_mode=True

class dates(BaseModel):
    date_from:date
    date_to:date
    @validator("date_from","date_to", pre=True)
    def prase_formatted_datetime(cls, value):
        return datetime.strptime(
            
            value,
             "%d-%m-%Y"
        )

class response(BaseModel):
    id:int
    formatted_datetime:str
    type_val:int
    detail:str
    amount:int

   
    class Config:
        orm_mode=True

