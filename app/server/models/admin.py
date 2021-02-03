from pydantic import BaseModel, Field, EmailStr


class AdminModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Yo Smol PP",
                "email": "smolpp@vppr.tech",
                "password": "Your password goes here."
            }
        }

def ResponseModel(data: dict, message: str):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error: str, code: int, message: str):
    return {
        "error": error,
        "code": code,
        "message": message
    }