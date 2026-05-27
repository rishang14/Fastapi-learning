from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from . import models,schema
from .database import init_db, get_db 
from typing import List 
from passlib.context import CryptContext 
from .route import post , user ,auth




pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield



app = FastAPI(lifespan=lifespan)


app.include_router(post.router) 
app.include_router(user.router) 
app.include_router(auth.router)

