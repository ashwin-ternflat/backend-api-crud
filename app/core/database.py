from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

def get_user_collection():
    return db["users"]
