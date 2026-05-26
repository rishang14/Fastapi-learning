from pydantic import BaseModel , EmailStr  


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
   email:EmailStr 


class CreateUser(UserBase): 
    password:str 

class User(UserBase): 
   id:int 
   class Config: 
      orm_mode=True


class AuthBase(BaseModel):  
   email:EmailStr 
   password:str 

class Signin(AuthBase): 
    pass   
    

class Signup(UserBase): 
    password:str  
    confirmPass:str