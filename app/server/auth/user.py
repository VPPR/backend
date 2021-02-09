from app.server.auth.jwt_bearer import JWTBearer
from app.server.auth.jwt_handler import decodeJWT
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from app.server.database.database import user_collection

security = HTTPBasic()
hash_helper = CryptContext(schemes=['bcrypt'])

async def validate_login(credentials: HTTPBasicCredentials = Depends(security)) -> bool:
    user = await user_collection.find_one({'email': credentials.username})
    if user:
        password = hash_helper.verify(credentials.password, user['password'])
        if not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password'
            )
        return True
    return False

async def validate_user_jwt(user: dict = Depends(decodeJWT(JWTBearer()))) -> bool:
    user = await user_collection.find_one({'email' : user['email']})
    if user:
        return True
    return False
