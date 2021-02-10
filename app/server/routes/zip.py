from fastapi.params import Depends
from app.server.auth.jwt_bearer import JWTBearer
from fastapi import Body, APIRouter, HTTPException, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext

from app.server.auth.user import validate_user_jwt, validate_login
from app.server.auth.jwt_handler import decodeJWT, signJWT
from app.server.database.database import add_user, delete_user, get_user
from app.server.models.user import UserModel

router = APIRouter()

hash_helper = CryptContext(schemes=['bcrypt'])

from zipfile import ZipFile
import pandas as pd
import io

filepath = '/home/prk/Downloads/Telegram Desktop/6009142927_1612802713907 (1).zip'
passwd = 'bATIPGnD'

# zipfile = ZipFile(file=filepath)

# for i in zipfile.namelist():
#     folder, filename = i.split('/')
#     if filename:
#         fileobj = zipfile.read(name=folder+'/'+filename, pwd=bytes(passwd, encoding='UTF-8'))
#         file = pd.read_csv(io.BytesIO(fileobj))
#         # print(file.head())
        # print(file.info())

@router.post('/upload_zip')
async def upload_zip(
    file : UploadFile = File(...),
    user : JWTBearer = Depends(JWTBearer())
):
    user = decodeJWT(user)
    if await validate_user_jwt(user):
        user = await get_user(user.get('email'))
        if user.get('is_admin'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='admin cannot upload zip'
            )
        else:
            file = await file.read()
            zipfile = ZipFile(io.BytesIO(file))
            for i in zipfile.namelist():
                folder, filename = i.split('/')
                if filename:
                    fileobj = zipfile.read(name=folder+'/'+filename, pwd=bytes(passwd, encoding='UTF-8'))
                    dataframe = pd.read_csv(io.BytesIO(fileobj))
                    if folder == 'ACTIVITY':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'SLEEP':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'BODY':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'USER':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'HEARTRATE':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'ACTIVITY_MINUTE':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'SPORT':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'ACTIVITY_STAGE':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')
                    elif folder == 'HEARTRATE_AUTO':
                        # insert code for particular file here
                        print(f'Folder name : {folder}, File Name : {filename}')