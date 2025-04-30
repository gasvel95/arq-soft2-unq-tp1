from domain.user_repository_interface import UserRepository
from domain.user import User
from repositories.mongo_connect import db
from bson import ObjectId

class UserRepositoryMongo(UserRepository):
    def __init__(self):
        self.collection = db["users"]

    def add(self, user: User) -> User:
        user_data = user.to_dict()
        result = self.collection.insert_one(user_data)
        user.id = str(result.inserted_id)
        return user

    def get(self, user_id: str) -> User:
        data = self.collection.find_one({"_id": ObjectId(user_id)})
        if not data:
            raise Exception("User not found")
        return User.entity_mapping(data)

    def update(self, user: User) -> User:
        self.collection.update_one(
            {"_id": ObjectId(user.id)}, {"$set": user.to_dict()}
        )
        return user

    def delete(self, user_id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(user_id)})
