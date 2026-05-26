from contextlib import asynccontextmanager
from fastapi import  HTTPException, status, Depends , APIRouter
from sqlalchemy.orm import Session
from .. import models,schema
from ..database import  get_db 
from typing import List  


router=APIRouter(
    prefix='/post', 
    tags=['Posts']

)

@router.get("/",response_model=List[schema.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
async def create_post(data: schema.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}",response_model=schema.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"data": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    db.delete(post)
    db.commit()


@router.put("/{id}",response_model=schema.Post)
async def update_post(id: int, data: schema.CreatePost, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post.title = data.title
    post.description = data.description
    db.commit()
    db.refresh(post)
    return {"data": post}
