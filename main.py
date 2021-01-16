import uvicorn

from typing import Optional, Dict
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, FastAPI
from fastapi.responses import Response
from models import UserIn, UserOut, UserPatch, create_user, get_users, user_helper, get_user, update_user_data, delete_user_data

app = FastAPI()
router = APIRouter()


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def error_response_model(error, code, message):
    return {"error": error, "code": code, "message": message}


@app.post("/create", response_model=UserOut)
def create_user_data(user: UserIn):
    print(user, 'before')
    user = jsonable_encoder(user)
    print(user, 'after')
    new_user = create_user(user)
    return Response(content=new_user, media_type="application/json")


@app.get("/users/")
def users_list():
    users = get_users()
    return users


@app.get("/users/{id}", response_description='User data retrieved')
def user_read(id: str):
    user = get_user(id)
    return user


@app.put("/users/{id}", response_description='User data updated')
def user_update(id: str, user: UserIn):
    user = {k: v for k, v in user.dict().items() if v is not None}  # <class 'models.UserIn'> -> <class 'dict'>
    updated_user = update_user_data(id, user)
    if updated_user:
        return response_model("User with ID: {} updated successfully".format(id),
                              "User updated successfully",
                              )
    return error_response_model(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@app.patch("/users/{id}", response_description='User data partially updated')
def user_partial_update(id: str, user: UserPatch):
    user = {k: v for k, v in user.dict().items() if v is not None}  # <class 'models.UserIn'> -> <class 'dict'>
    updated_user = update_user_data(id, user)
    if updated_user:
        return response_model("User with ID: {} updated successfully".format(id),
                              "User updated successfully",
                              )
    return error_response_model(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@app.delete("/users/{id}", response_description='User data deleted')
def user_delete(id: str):
    deleted_user = delete_user_data(id)
    if deleted_user:
        return response_model("User with ID: {} deleted successfully".format(id),
                              "User deleted successfully",
                              )
    return error_response_model(
        "An error occurred",
        404,
        "Student doesn't exist",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
