from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Post schemas
class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    author_id: int
    author: UserResponse

    class Config:
        from_attributes = True


# Comment schemas
class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author_id: int
    post_id: int
    author: UserResponse

    class Config:
        from_attributes = True


class PostWithComments(PostResponse):
    comments: List[CommentResponse] = []
