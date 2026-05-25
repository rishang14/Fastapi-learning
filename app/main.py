from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from .database import init_pool, init_db, get_db

class Post(BaseModel):
    title: str
    description: str


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_pool()
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/posts")
async def get_posts(conn=Depends(get_db)):
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {"data": posts}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(data: Post,conn=Depends(get_db)): 
    cur=conn.cursor() 
    cur.execute("INSERT INTO POSTS (title , description) VALUES (%s , %s) RETURNING *",
                (data.title, data.description))  
    
    new_post= cur.fetchone() 
    conn.commit()
    return {"message": new_post}


@app.get("/posts/{id}")
async def get_post(id: int):
    if id != 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="pls enter valid id")
    return {"data": "here is ur post"}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    if id != 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")


@app.put("/posts/{id}")
async def update_post(id: int,):
    if id != 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item {id} not found")
    return {"data": "item updated successfully"}
