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