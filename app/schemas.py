from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class post(BaseModel):
    title: str
    content: str
    published: bool = True

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime  

    class Config:
        from_attributes = True

class post_reponse(post):
    id: int
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: post_reponse  # Assuming you have a standard 'Post' schema defined above this
    votes: int

    # Add this configuration so Pydantic knows how to read the SQLAlchemy tuple!
    model_config = ConfigDict(from_attributes=True)

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class login(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: str

class token(BaseModel):
    token: str
    token_type: str

class vote(BaseModel):
    post_id: int
    dir: int= Field(ge=0, le=1)