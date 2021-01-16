from typing import Optional, Dict
from pydantic import BaseModel, Field
from pymongo import MongoClient
import datetime
from bson import ObjectId, json_util, SON


client = MongoClient('localhost', 27017)
db = client['Emphasoft-database']
collection = db['Emphasoft-collection']


class UserIn(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    last_login: datetime.datetime
    is_superuser: bool = False


class UserPatch(BaseModel):
    username: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool]
    last_login: Optional[datetime.datetime]
    is_superuser: Optional[bool]


class UserOut(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_active: bool = True
    last_login: datetime.datetime
    is_superuser: bool = False


class UserInDB(UserIn):
    hashed_password: str


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "is_active": user["is_active"],
        "last_login": user["last_login"],
        "is_superuser": user["is_superuser"],
    }


def create_user(data):
    user = collection.insert_one(data)
    new_user = collection.find_one({'_id': user.inserted_id})
    return json_util.dumps(new_user)


def get_users():
    users = []
    for user in collection.find():
        users.append(user_helper(user))
    return users


def get_user(id: str) -> dict:
    user = collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


def update_user_data(id: str, data):
    if len(data) < 1:   # Check body is not empty
        return False
    user = collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = collection.update_one(
                    {"_id": ObjectId(id)}, {"$set": data}
                )
        if updated_user:
            return True
        return False


def delete_user_data(id: str):
    user = collection.find_one({"_id": ObjectId(id)})
    if user:
        collection.delete_one({"_id": ObjectId(id)})
        return True
