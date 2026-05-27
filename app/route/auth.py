from fastapi import  HTTPException, status, Depends , APIRouter   
from datetime import timedelta
from sqlalchemy.orm import Session
from .. import models,schema   
from ..utils import pwd_context 
from ..database import get_db  
from ..utils import create_token ,decode_token


router=APIRouter(
    prefix="/auth", 
    tags=['Auth']
) 



@router.post("/signin") 
async def signin(data:schema.Signin,db:Session=Depends(get_db)):   
     user=db.query(models.User).filter(models.User.email == data.email).first()  

     if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this {data.email} email not found ")
    
     isSame= pwd_context.verify(data.password,user.password) 

     if not isSame : 
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"Invalid Credentials") 
     
    #  print(create_token(data={"user_id": user.id, "user.name":user.name , "user.email":user.email},
    #   expires_delta=timedelta(minutes=30)))  

     print("token" , decode_token("yJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJ1c2VyLm5hbWUiOiJ0ZXN0IiwidXNlci5lbWFpbCI6ImRlbW9AZW1haWwuY29tIiwiZXhwIjoxNzc5NzgwMDQ3fQ.VXOgho9XGr-NR84gEMHfaCBS2AYbyFTWqyWvLk9hQ0E"))

     return {"data":"login successful"}


@router.post("/signup") 
async def signup(data:schema.Signin, db:Session=Depends(get_db)):  
   return {"data": "signup successful"}


