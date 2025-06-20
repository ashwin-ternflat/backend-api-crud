from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserInDB
from app.core.database import get_user_collection
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserInDB, status_code=201)
def create_user(user: UserCreate):
    user_collection = get_user_collection()
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user_dict = user.dict()
    user_dict["created_at"] = user_dict.get("created_at")
    result = user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserInDB(**user_dict)

@router.get("/", response_model=list[UserInDB])
def get_all_users():
    user_collection = get_user_collection()
    users = list(user_collection.find())
    for user in users:
        user["id"] = str(user["_id"])
    return [UserInDB(**user) for user in users]
