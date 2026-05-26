from contextlib import asynccontextmanager
from fastapi import  HTTPException, status, Depends , APIRouter
from sqlalchemy.orm import Session
from .. import models,schema
from ..database import  get_db   
from ..utils import pwd_context




router=APIRouter(
    prefix='/user', 
    tags=['Users']
)


@router.get("/{id}",response_model=schema.User)
async def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return  user


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.User)
async def create_user(data: schema.CreateUser, db: Session = Depends(get_db)): 

    hased_pass= pwd_context.hash(data.password) 
    data.password=hased_pass
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user 

