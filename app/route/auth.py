from fastapi import  HTTPException, status, Depends , APIRouter  
from sqlalchemy.orm import Session
from .. import models,schema   

from ..database import get_db 


router=APIRouter(
    prefix="/auth", 
    tags=['Auth']
) 



@router.post("/signin") 
async def signin(data:schema.Signin,db:Session=Depends(get_db)):  

    return {"data":"login successful"}


@router.post("/signup") 
async def signup(data:schema.Signin, db:Session=Depends(get_db)):  
   user=db.query(models.User).filter(models.User.email == data.email).first()  

   if not user : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with this {data.email} email not found ")
    
    
   return {"data": "signup successful"}


