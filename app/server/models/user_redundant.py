from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    phone: int = Field(...)


    class Config:
        schema_extra = {
            "example": {
                "fullname": "Yo Smol PP",
                "email": "smolpp@vppr.tech",
                "phone": 9999999999
            }
        }


class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Yo Smol PP",
                "email": "smolpp@vppr.tech",
                "phone": 9999999999
            }
        }


def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }