from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database.database import *
from app.server.models.user import *

router = APIRouter()


@router.get("/", response_description="users retrieved")
async def get_users():
    users = await retrieve_users()
    return ResponseModel(users, "users data retrieved successfully") \
        if len(users) > 0 \
        else ResponseModel(
        users, "Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    return ResponseModel(user, "user data retrieved successfully") \
        if user \
        else ErrorResponseModel("An error occured.", 404, "user doesn'exist.")


@router.post("/", response_description="user data added into the database")
async def add_user_data(user: userModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "user added successfully.")


@router.delete("/{id}", response_description="user data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    return ResponseModel("user with ID: {} removed".format(id), "user deleted successfully") \
        if deleted_user \
        else ErrorResponseModel("An error occured", 404, "user with id {0} doesn't exist".format(id))


@router.put("{id}")
async def update_user(id: str, req: UpdateUserModel = Body(...)):
    updated_user = await update_user_data(id, req.dict())
    return ResponseModel("user with ID: {} name update is successful".format(id),
                         "user name updated successfully") \
        if updated_user \
        else ErrorResponseModel("An error occurred", 404, "There was an error updating the user.".format(id))