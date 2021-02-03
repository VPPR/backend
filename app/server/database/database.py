import motor.motor_asyncio
from bson import ObjectId
from decouple import config

from typing import Optional

from app.server.database.database_helper import user_helper, admin_helper

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.users

user_collection = database.get_collection('users_collection')
admin_collection = database.get_collection('admins')

async def add_admin(admin_data: dict) -> Optional[dict]:
    # add admin if email not present already
    # param admin_data : dict -> contains keys fullname, email, password
    # return
    #       dict -> return user details
    #       None -> if email was already present
    admin = await admin_collection.find_one({'email':admin_data.get('email')})
    if admin == None:
        admin = await admin_collection.insert_one(admin_data)
        new_admin = await admin_collection.find_one({"_id": admin.inserted_id})
        return admin_helper(new_admin)
    return None

async def delete_admin(email: str) -> Optional[dict]:
    admin = await admin_collection.find_one({'email':email})
    if admin:
        await admin_collection.delete_one({'email':email})
        return admin_helper(admin)
    else:
        return None

async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_user_data(id: str, data: dict):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        user_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return True