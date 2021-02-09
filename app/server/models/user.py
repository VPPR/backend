from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    phone: int = Field(...)
    is_admin: bool = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'fullname': 'Yo Smol PP',
                'email': 'smolpp@vppr.tech',
                'password': 'thingthatyoualwaysforget',
                'phone' : '6942069420',
                'is_admin' : True
            }
        }