from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
import os

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["backend_api_db"]
collection = db["users"]


# Pydantic model

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    age: Optional[int] = None


def serialize_user(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "age": user.get("age")
    }

# API Router with CRUD

router = APIRouter()

@router.post("/users", response_model=User)
def create_user(user: User):
    user_dict = user.dict(exclude={"id"})
    result = collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

@router.get("/users", response_model=List[User])
def get_users():
    users = list(collection.find())
    return [serialize_user(u) for u in users]

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    user = collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return serialize_user(user)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: User):
    updated = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict(exclude={"id"})}
    )
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    user_updated = collection.find_one({"_id": ObjectId(user_id)})
    return serialize_user(user_updated)

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    deleted = collection.delete_one({"_id": ObjectId(user_id)})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"message": "User deleted"})


# FastAPI App

app = FastAPI()
app.include_router(router)
