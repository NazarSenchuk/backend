
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Body, Depends, HTTPException
from pydantic import validator
from sqlalchemy import Column, Integer, String
import re
from app.db import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)






class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)


    
    def validate_password(password, **kwargs):

        if len(password) < 8:
            return{"error": "Make sure your password is at lest 8 letters"}
        elif re.search('[0-9]',password) is None:
            return{"error": "Make sure your password has a number in it"}
        elif re.search('[A-Z]',password) is None: 
            return{"error": "Make sure your password has a capital letter in it"}
        return password

    







class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)


    class Config:
        json_schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",

            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }
