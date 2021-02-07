from fastapi import Body, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from app.server.auth.admin import validate_login
from app.server.auth.jwt_handler import signJWT
from app.server.database.database import add_admin, delete_admin
from app.server.models.admin import *
from app.server.database.database import admin_collection

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def admin_login(admin: HTTPBasicCredentials = Body(...)):
    if await validate_login(admin):
        return {
            "email": admin.username,
            "access_token": signJWT(admin.username)
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials"
    )

@router.post("/signup")
async def admin_signup(admin: AdminModel = Body(...)):
    # retrive the first record that matches with the email in request
    # if no records found, create new user
    # otherwise raise 409 error
    admin.password = hash_helper.encrypt(admin.password)
    new_admin = await add_admin(jsonable_encoder(admin))
    if new_admin == None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    else:
        return new_admin

@router.post('/delete')
async def admin_delete(admin: HTTPBasicCredentials = Body(...)):
    if await validate_login(admin):
        deleted_admin = await delete_admin(admin.username)
        return deleted_admin
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )