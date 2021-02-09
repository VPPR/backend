import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from typing import Dict, Optional

from app.server.database.database_helper import user_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection('users')

async def add_user(user_data: dict) -> Optional[dict]:
    # add user if email not present already
    # param user_data : dict -> contains keys fullname, email, password
    # return
    #       dict -> return user details
    #       None -> if email was already present
    user = await user_collection.find_one({'email':user_data.get('email')})
    if user == None:
        user = await user_collection.insert_one(user_data)
        user = await user_collection.find_one({'_id': user.inserted_id})
        return user_helper(user)
    return None

async def get_user(email: str) -> Optional[dict]:
    user = await user_collection.find_one({'email':email})
    if user != None:
        return user_helper(user)
    return None

async def delete_user(email: str) -> Optional[dict]:
    user = await user_collection.find_one({'email':email})
    if user:
        await user_collection.delete_one({'email':email})
        return user_helper(user)
    else:
        return None

async def retrieve_users(is_admin: bool = False) -> Dict:
    # retrive either normal users, or admins
    # param is_admin : bool -> determines if function will
    # return list of admins or normal users
    users = []
    async for user in user_collection.find():
        if user.is_admin == is_admin: 
           users.append( user_helper(user))
    return users


# async def add_user(user_data: dict) -> dict:
#     user = await user_collection.insert_one(user_data)
#     new_user = await user_collection.find_one({'_id': user.inserted_id})
#     return user_helper(new_user)

# async def retrieve_user(id: str) -> dict:
#     user = await user_collection.find_one({'_id': ObjectId(id)})
#     if user:
#         return user_helper(user)

# async def delete_user(id: str):
#     user = await user_collection.find_one({'_id': ObjectId(id)})
#     if user:
#         await user_collection.delete_one({'_id': ObjectId(id)})
#         return True

# async def update_user_data(id: str, data: dict):
#     user = await user_collection.find_one({'_id': ObjectId(id)})
#     if user:
#         user_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
#         return True