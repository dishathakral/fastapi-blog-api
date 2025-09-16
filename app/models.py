from typing import Optional
from pydantic import BaseModel, Field,EmailStr


class Usercreate (BaseModel):
    email: EmailStr
    password:str   

class Userout(BaseModel):
    id:int
    email:str
    class Config:
        from_attributes = True
class Userlogin(BaseModel):
    email:EmailStr
    password:str

class PostBase (BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase) :
    pass

class PostResponse(BaseModel):
    title: str = Field(..., alias="name")
    content:str
    published:bool
    owner_id:int
    owner:Userout
    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str 
    token_type: str
class TokenData (BaseModel):
    id: Optional[int]    