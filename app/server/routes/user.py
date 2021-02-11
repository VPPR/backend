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

hash_helper = CryptContext(schemes=['bcrypt'])

@router.post('/login', name="Login",
    description='''Route for user login. 
        Accepts username and password and returns JWT Token and Expiry time''')
async def user_login(user: HTTPBasicCredentials = Body(...)):
    if await validate_login(user):
        user = await get_user(user.username)
        return signJWT(user.get('email'))
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid credentials'
    )

@router.post('/signup',name="Signup",
    description='''Route for user registration. 
        Accepts username, password, fullname, phone number and is_admin and
         returns the created user or the error message''')
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

@router.get('/self',name="Get Self details", description="Gets the details for the calling user",)
async def get_user_self(user : JWTBearer = Depends(JWTBearer())):
    user = decodeJWT(user)
    return await get_user(user.get('email'))
# NEED TO REWRITE
@router.post('/delete/self', name="Delete self", description="Deletes the calling user from the database")
async def user_delete_self(user : JWTBearer = Depends(JWTBearer())):
    user = decodeJWT(user)
    if await validate_user_jwt(user):
        deleted_user = await delete_user(user.get('email'))
        print(delete_user)
        return deleted_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
#NEED TO REWRITE TO GET PARAM FROM URL
@router.post('/delete')
async def user_delete(admin : JWTBearer = Depends(JWTBearer()), email: str = Body(...)):
    # here I'm writing user as admin because only admin will use this path
    # check if user is authenticated
    # then check if user is admin
    # then check if email that is to be deleted exsts, if not, return 404
    # then check if that email to be deleted belongs to admin type user, if it does, then retun 401
    # then delete the user with given email id and return his details
    admin = decodeJWT(admin)
    if await validate_user_jwt(admin):
        admin = await get_user(admin.get('email'))
        if admin.get('is_admin'):
            user = await get_user(email)
            if user == None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='user does not exists'
                )
            if user.get('is_admin'):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='cannot delete admin'
                )
            deleted_user = await delete_user(email)
            return deleted_user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='you need to be admin to perform this operation'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid credentials'
        )
