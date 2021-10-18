# app/model.py

from pydantic import BaseModel, Field


# class PostSchema(BaseModel):
#     id: int = Field(default=None)
#     title: str = Field(...)
#     content: str = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "title": "Securing FastAPI applications with JWT.",
#                 "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
#             }
#         }

class UserSchema(BaseModel):
    fullname: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Anita Satria Dewi Fina",
                "username": "asdf",
                "password": "asdf"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "asdf",
                "password": "asdf"
            }
        }