from fastapi.params import Depends
from app.server.auth.jwt_bearer import JWTBearer
from fastapi import Body, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from app.server.auth.user import validate_user_jwt, validate_login
from app.server.auth.jwt_handler import decodeJWT, signJWT
from app.server.database.database import add_user, delete_user, get_user
from app.server.models.user import UserModel

router = APIRouter()
auth_router = APIRouter()

hash_helper = CryptContext(schemes=['bcrypt'])

@router.post('/login')
async def user_login(user: HTTPBasicCredentials = Body(...)):
    if await validate_login(user):
        user = await get_user(user.username)
        print(user)
        return {
            'email': user.get('email'),
            'is_admin' : user.get('is_admin'),
            'access_token': signJWT(user.get('email'))
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid credentials'
    )

@router.post('/signup')
async def user_signup(user: UserModel = Body(...)):
    # retrive the first record that matches with the email in request
    # if no records found, create new user
    # otherwise raise 409 error
    user.password = hash_helper.encrypt(user.password)
    user = await add_user(jsonable_encoder(user))
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exists'
        )
    else:
        return user

@auth_router.post('/delete/self')
async def user_delete_self(user: HTTPBasicCredentials = Body(...)):
    if await validate_login(user):
        deleted_user = await delete_user(user.username)
        print(delete_user)
        return deleted_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )

@auth_router.post('/delete')
async def user_delete(admin : dict = Depends(JWTBearer()), user_id: str = Body(...)):
    if await validate_user_jwt(decodeJWT(admin)):
        deleted_user =await delete_user(user_id)
        print(delete_user)
        return deleted_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
