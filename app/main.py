from fastapi import FastAPI, Query , HTTPException , status
from fastapi.responses import PlainTextResponse 
import yaml
import tempfile
from typing import Literal ,Optional
from pydantic import BaseModel 



class Post(BaseModel): 
   title: str
   desc : str   

app = FastAPI()

@app.get("/") 
async def root():
    return {"message": "Hello"} 

@app.get("/posts") 
async def get_posts():  
     return {"data":"Here is ur posts"} 


@app.post("/createpost",status_code=status.HTTP_201_CREATED) 
async def create_post(post:Post): 
    print(post)
    return {'message':"Your created posts"} 


@app.get("/posts/{id}") 
async def getPosts(id:int):  
    if id != 2:  
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"pls enter valid id") 
     
    return {"data":"here is ur post"} 




@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
async def deletePost(id:int): 
    if id != 2: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"item {id} not found") 

    return {"data":"item deleted successfully"} 




@app.put("/posts/{id}") 
async def updateposts(id:int,data:Post): 
      if id  != 2: 
          raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                              detail= f"  item {id } not found") 
      
      return {"data":"item updated successfully"}