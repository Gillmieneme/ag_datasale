from fastapi import FastAPI,Request, status
from sqlalchemy.orm import Session,column_property
from sqlalchemy import asc
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from .database import engine
from .import models, schema,auth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy import func
from sqlalchemy.sql import text
import sqlalchemy as bb

models.base.metadata.create_all(bind=engine)
app=FastAPI()
# origions=["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#domains which 
    allow_credentials=True,
    allow_methods=["*"],# allow specific mehods(get,update)
    allow_headers=["*"],#allwo which headers
)

@app.get('/')
def home():
   return{
      "message":"we are in home baby"
   }

@app.post("/get",response_model=List[schema.response])
def get_posts(d:schema.dates, db: Session=Depends(get_db),current_user:int =Depends(auth.get_current_user)):
    dd=d.dict()
    dd['date_from'] = dd['date_from'].strftime("%Y/%m/%d")
    dd['date_to'] = dd['date_to'].strftime("%Y/%m/%d")
    postes=db.query(models.Income).filter(models.Income.user_id==current_user.id,models.Income.dates >= dd['date_from'] ,models.Income.dates <= dd['date_to'],models.Income.is_deleted==False).order_by(models.Income.dates.asc()).all()
    return postes


@app.get("/latest")
def get_posts( db: Session=Depends(get_db),current_user:int =Depends(auth.get_current_user)):
    
    query = db.query(models.Income.amount).filter(models.Income.is_deleted==False,models.Income.user_id==current_user.id,models.Income.type_val==1).all()
    query_exp=db.query(models.Income.amount).filter(models.Income.is_deleted==False,models.Income.user_id==current_user.id,models.Income.type_val==2).all()
    query_pay=db.query(models.Income.amount).filter(models.Income.is_deleted==False,models.Income.user_id==current_user.id,models.Income.type_val==3).all()
    a=0
    b=0
    c=0
    for i in query:
       a=a+i[0]
    print(a)
    for i in query_exp:
       b=b+i[0]

    for i in query_pay:
       c=c+i[0]
    profit=a-(b+c)  
    
    return  profit


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(income:schema.Income,db: Session=Depends(get_db),current_user:int =Depends(auth.get_current_user)):
    
    incomes=income.dict()
    incomes['dates'] = incomes['dates'].strftime("%Y/%m/%d")
    print(incomes["detail"])
    if incomes["detail"]=='':
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no detail given")
   
    
    incomes["user_id"]=current_user.id
    new_post=models.Income(**incomes)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return ("hi")



@app.put("/delete/{id}")
def delete_post(id:int,db: Session = Depends(get_db),current_user:int =Depends(auth.get_current_user)): #id is integer
    print(id)
    id_user=current_user.id
    post= db.query(models.Income).filter(models.Income.id==id,models.Income.user_id==id_user).first()
    post.is_deleted=True
    
 
    db.commit()
    return ("Post deleted")


@app.post("/user",status_code=status.HTTP_201_CREATED, response_model=schema.UserResponce)
def create_user(new_user:schema.UserCreate,db: Session = Depends(get_db)):
   #has the password- user.passowrd
   hashed_password=auth.hash(new_user.password)
   new_user.password= hashed_password

   user=models.User(**new_user.dict())
   db.add(user)
   db.commit()
   db.refresh(user)
   return user




@app.post('/login', response_model=schema.Token)
def login( user_credentials:schema.UserLogin, db:Session = Depends(get_db)):
 user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
 if not user:
  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")
 
 if not auth.verify( user_credentials.password,user.password): #if it is true, returns token,,,,if not it raises an exception
  raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

 access_token=auth.create_access_token(data={"user_id": user.id})
 return{"access_token": access_token, "token_type":"bearer"}
