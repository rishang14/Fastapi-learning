from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import models,schema
from .database import init_db, get_db 
from typing import List 
from passlib.context import CryptContext




pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield



app = FastAPI(lifespan=lifespan)



@app.get("/posts",response_model=List[schema.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


@app.post("/post", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
async def create_post(data: schema.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@app.get("/posts/{id}",response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    db.delete(post)
    db.commit()


@app.put("/posts/{id}",response_model=schema.Post)
async def update_post(id: int, data: schema.CreatePost, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post.title = data.title
    post.description = data.description
    db.commit()
    db.refresh(post)
    return {"data": post}




@app.get("/user/{id}",response_model=schema.User)
async def get_users(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    return  user


@app.post("/user", status_code=status.HTTP_201_CREATED,response_model=schema.User)
async def create_usert(data: schema.CreateUser, db: Session = Depends(get_db)): 

    hased_pass= pwd_context.hash(data.password) 
    data.password=hased_pass
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user 

