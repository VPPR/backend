from fastapi import Body, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from app.server.auth.admin import validate_login
from app.server.auth.jwt_handler import signJWT
from app.server.database.database import add_admin
from app.server.models.admin import AdminModel
from app.server.database.database import admin_collection

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/login")
async def admin_login(admin: HTTPBasicCredentials = Body(...)):
    if await validate_login(admin):
        return signJWT(admin.username)
    return "Invalid Login Details!"

@router.post("/")
async def admin_signup(admin: AdminModel = Body(...)):
    # retrive the first record that matches with the email in request
    # if no records found, create new user
    # otherwise raise 409 error
    old_admin = await admin_collection.find_one({'email': admin.email})
    if old_admin == None:
        admin.password = hash_helper.encrypt(admin.password)
        new_admin = await add_admin(jsonable_encoder(admin))
        return new_admin
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )