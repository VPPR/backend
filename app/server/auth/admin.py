from app.server.auth.jwt_bearer import JWTBearer
from app.server.auth.jwt_handler import decodeJWT
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext

from app.server.database.database import admin_collection

security = HTTPBasic()
hash_helper = CryptContext(schemes=["bcrypt"])

async def validate_login(credentials: HTTPBasicCredentials = Depends(security)):
    admin = await admin_collection.find_one({"email": credentials.username})
    if admin:
        password = hash_helper.verify(credentials.password, admin['password'])
        if not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        return True
    return False

async def validate_admin_jwt(admin: dict = Depends(decodeJWT(JWTBearer()))):
    db_admin=await admin_collection.find_one({"email":admin["user_id"]})
    if db_admin:
        return True
    return False
