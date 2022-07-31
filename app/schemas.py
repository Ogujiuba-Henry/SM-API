from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class Post(BaseModel):  # specifies what the body of post should look like
      title: str 
      content: str 
      published: bool
      class Config:
            orm_mode=True #Pydantic reads only dict, convert sqlalchemy model to pydantic model

class UserResponse(BaseModel):
      id: int
      email:EmailStr
      created_at:datetime

      class Config:
            orm_mode=True


class PostResponse(Post):   # specifies exact data you send back to client || inherirts validations from the First Post class
    id: int
    created_at:datetime
    user_id:int
    owner:UserResponse


class PostOut(BaseModel):
      Post:PostResponse                #Bcos the response adds a Post: variable @postman so we added it to reference the original Post class
      votes:int
      
      class Config:
            orm_mode=True


class UserCreate(BaseModel):
      email:EmailStr                   # ensure that it is a valid email
      password:str
    

class UserLogin(BaseModel):
      email:EmailStr
      password:str


class Token(BaseModel):
      access_token:str
      token_type:str

class TokenData(BaseModel):
      id:Optional[str] = None

class Vote(BaseModel):
      post_id:int
      dir:conint(le=1)    #allows for only numbers less than 1


