from pydantic import BaseModel 


class PostBase(BaseModel):
    title: str
    description: str


class CreatePost(PostBase): 
  pass 

class Post(PostBase): 
   id:int 

   class Config: 
      orm_mode=True



class UserBase(BaseModel): 
   name:str 
   email:str 


class CreateUser(UserBase): 
    password:str 

class User(UserBase): 
   id:int 

   class Config: 
      orm_mode=True

